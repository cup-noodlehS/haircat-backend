from general.models import File, Location
from general.base_serializers import FileBaseSerializer, LocationBaseSerializer
from haircat.utils import GenericView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .webhooks import send_webhook


class FileView(GenericView):
    serializer_class = FileBaseSerializer
    queryset = File.objects.all()
    permission_classes = [AllowAny]  # Allow unauthenticated access for file uploads


class LocationView(GenericView):
    serializer_class = LocationBaseSerializer
    queryset = Location.objects.all()


class TestWebhookView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """
        Test sending a webhook to the authenticated user
        
        POST data:
        - event_name: Name of the event
        - data: Data to send with the event
        """
        event_name = request.data.get('event_name', 'test_event')
        data = request.data.get('data', {})
        user_id = str(request.user.id)
        
        # Send the webhook
        success = send_webhook(event_name, user_id, data)
        
        if success:
            return Response({'status': 'success', 'message': 'Webhook sent'}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'error', 'message': 'Failed to send webhook'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
