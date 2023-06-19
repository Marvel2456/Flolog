from django.shortcuts import render
from allauth.socialaccount.providers.oauth2.views import OAuth2Adapter
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
    adapter = OAuth2Adapter(provider_id='google')
    # provider = adapter.get_provider()
    token = request.data.get('access_token')
    email = request.data.get('email')
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')

    if token:
        login_token = adapter.parse_token({'access_token': token})
        login_token.token_secret = ''
        user = adapter.authenticate(request, login_token)
        if user:
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
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
