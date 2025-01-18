from django.utils.functional import SimpleLazyObject
from django.contrib.auth.middleware import get_user
from rest_framework_simplejwt.authentication import JWTAuthentication


def get_user_jwt(request):
    user = None
    try:
        authentication = JWTAuthentication()
        user_auth_tuple = authentication.authenticate(request)
        if user_auth_tuple is not None:
            user = user_auth_tuple[0]
    except:
        pass
    return user


class JWTAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.user = SimpleLazyObject(lambda: self._get_user(request))
        return self.get_response(request)

    def _get_user(self, request):
        if not hasattr(request, "_cached_user"):
            request._cached_user = get_user(request)
            if request._cached_user.is_anonymous:
                jwt_user = get_user_jwt(request)
                if jwt_user is not None:
                    request._cached_user = jwt_user
        return request._cached_user
