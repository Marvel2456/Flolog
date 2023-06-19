from django.shortcuts import render
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

@api_view(['POST'])
@permission_classes([AllowAny])
def social_auth(request):
    adapter = GoogleOAuth2Adapter(request)
    provider = adapter.get_provider()
    token = request.data.get('access_token')

    if token:
        user = adapter.authenticate(request, provider, token)
        if user:
            user.is_client = True
            user.is_google_user = True
            user.save()

            # Generate the access token
            refresh_token = RefreshToken.for_user(user)
            access_token = refresh_token.access_token

            return Response({
                'access_token': str(access_token),
                'refresh_token': str(refresh_token),
                'detail': 'Successfully authenticated.'
            })
        else:
            return Response({'detail': 'Authentication failed.'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'detail': 'Access token not provided.'}, status=status.HTTP_400_BAD_REQUEST)