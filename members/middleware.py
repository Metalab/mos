from django.contrib.auth import logout


class DeactivateUserMiddleware(object):
    def process_request(self, request):
        if request.user.is_authenticated() and not request.user.is_active:
                        return logout(request)
