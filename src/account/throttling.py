from rest_framework.throttling import SimpleRateThrottle


class UserLoginRateThrottle(SimpleRateThrottle):
    rate = "10/hour"
    scope = "user_login"

    def get_cache_key(self, request, view):
        username = request.data.get("username", "")
        ip = self.get_ident(request)
        return self.cache_format % {"scope": self.scope, "ident": f"{username}-{ip}"}
