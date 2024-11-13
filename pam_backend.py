import os
import django

# Set the settings module environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'librephotos.settings.production')  # Adjust accordingly

# Setup Django
django.setup()

from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
import pam

class PAMBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        p = pam.pam()
        if p.authenticate(username, password):
            try:
                user = User.objects.get(username=username)
                return user
            except User.DoesNotExist:
                return None
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
