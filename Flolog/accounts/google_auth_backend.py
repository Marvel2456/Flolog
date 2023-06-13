# google_auth_backend.py
from django.contrib.auth.backends import BaseBackend
from .models import CustomUser
from django.conf import settings
from google_auth_oauthlib.flow import Flow
from google.auth.transport import requests
from google.oauth2.id_token import verify_oauth2_token

class GoogleAuthBackend(BaseBackend):
    def authenticate(self, request, id_token=None):
        # Verify the Google ID token
        try:
            id_info = verify_oauth2_token(
                id_token, requests.Request(), settings.GOOGLE_CLIENT_ID
            )
            # Extract the user's email from the ID token and create or retrieve the user
            email = id_info['email']
            user, created = CustomUser.objects.get_or_create(email=email)
            if created:
                user.username = id_info['sub']
                # Set is_client to True for newly created user
                user.is_client = True
                # Set is_google_user to True for newly created user
                user.is_google_user = True  
                
                user.save()
            elif not user.is_client:
                raise ValueError('User is not allowed to sign in with Google.')
            else:
                # Set is_google_user to True for existing user
                user.is_google_user = True  
                user.save()
            return user
        except Exception as e:
            # Handle verification error
            return None

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None
