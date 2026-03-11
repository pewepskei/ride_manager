from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from rides.models import User

class SimpleHeaderAuthentication(BaseAuthentication):
    """
    Authentication that checks for header:
    X-User-Email: <email>
    X-User-Role: admin
    """

    def authenticate(self, request):
        email = request.headers.get('X-User-Email')
        role = request.headers.get('X-User-Role')
        if not email or not role:
            return None  # DRF will return 401 automatically

        try:
            user = User.objects.get(email=email, role=role)
            return (user, None)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid credentials')
