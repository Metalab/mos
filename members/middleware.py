from django.contrib.auth import logout
from django.utils.deprecation import MiddlewareMixin

class DeactivateUserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated() and not request.user.is_active:
                        return logout(request)
