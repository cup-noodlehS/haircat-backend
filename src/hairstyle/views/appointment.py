from hairstyle.serializers.appointment import (
    AppointmentSerializer,
    ReviewImageSerializer,
    ReviewSerializer,
)
from hairstyle.serializers.appointment_message import (
    AppointmentMessageThreadSerializer,
    AppointmentMessageSerializer,
)
from hairstyle.models.appointment import (
    Appointment,
    Review,
    ReviewImage,
    AppointmentMessageThread,
    AppointmentMessage,
)
from haircat.utils import GenericView
from rest_framework.permissions import IsAuthenticated
from django.db import models
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from django.core.cache import cache
from django.core.paginator import Paginator
from django.db.models import Q



class AppointmentView(GenericView):
    serializer_class = AppointmentSerializer
    queryset = Appointment.objects.all()


class ReviewView(GenericView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()


class ReviewImageView(GenericView):
    serializer_class = ReviewImageSerializer
    queryset = ReviewImage.objects.all()
    allowed_methods = ["list", "create", "delete"]


class AppointmentMessageThreadView(GenericView):
    serializer_class = AppointmentMessageThreadSerializer
    queryset = AppointmentMessageThread.objects.all()
    allowed_methods = ["list", "create", "retrieve"]
    permission_classes = [IsAuthenticated]

    def initialize_queryset(self, request):
        self.queryset = self.queryset.filter(Q(appointment__customer__user=request.user) | Q(appointment__service__specialist__user=request.user))

    def filter(self, request, filters, excludes, top, bottom, order_by=None):
        self.queryset = (
            self.queryset.annotate(
                latest_message_created_at=models.Max("Messages__created_at")
            )
            .filter(Messages__isnull=False)
            .distinct()
            .order_by("-latest_message_created_at")
        )

        queryset = self.filter_queryset(filters, excludes)

        if order_by:
            queryset = queryset.order_by(order_by)

        paginator = Paginator(queryset, self.size_per_request)
        page_number = (top // self.size_per_request) + 1
        page = None
        if bottom is None:
            page = paginator.get_page(page_number)
        else:
            page = queryset[top:bottom]

        serializer = self.serializer_class(
            page, many=True, context={"request": request}
        )
        data = None
        if bottom is None:
            data = {
                "objects": serializer.data,
                "total_count": paginator.count,
                "num_pages": paginator.num_pages,
                "current_page": page.number,
            }
        else:
            data = {
                "objects": serializer.data,
                "total_count": queryset.count(),
            }

        cache_key = self.get_list_cache_key(filters, excludes, top, bottom, order_by)
        cache.set(cache_key, data, self.cache_duration)

        return Response(data, status=status.HTTP_200_OK)


class AppointmentMessageView(GenericView):
    serializer_class = AppointmentMessageSerializer
    queryset = AppointmentMessage.objects.all()
    allowed_methods = ["list", "create"]
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["post"])
    def send_message(self, request, thread_id=None):
        if not thread_id:
            return Response(
                {"error": "thread_id is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            thread = AppointmentMessageThread.objects.get(id=thread_id)
            thread.mark_unread_messages(request.user)
        except AppointmentMessageThread.DoesNotExist:
            return Response(
                {"error": "Thread not found"}, status=status.HTTP_404_NOT_FOUND
            )

        # Create a mutable copy of the request data
        mutable_data = request.data.copy()
        mutable_data["sender_id"] = request.user.id
        mutable_data["appointment_message_thread_id"] = thread_id

        # Update the request object with the modified data
        request._full_data = mutable_data

        return self.create(request)

    @action(detail=False, methods=["get"])
    def list(self, request, thread_id=None):
        if "list" not in self.allowed_methods:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

        if not thread_id:
            return Response(
                {"error": "thread_id is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        thread = get_object_or_404(AppointmentMessageThread, id=thread_id)
        thread.mark_unread_messages(request.user)
        try:
            filters, excludes = self.parse_query_params(request)
            top, bottom, order_by = self.get_pagination_params(filters)

            cached_data = None
            if self.cache_key_prefix:
                cache_key = self.get_list_cache_key(
                    filters, excludes, top, bottom, order_by
                )
                cached_data = cache.get(cache_key)
            if cached_data:
                return Response(cached_data, status=status.HTTP_200_OK)

            return self.filter(request, filters, excludes, top, bottom, order_by)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
