from django.shortcuts import render
from .serializers import ClientRegistrationSerializer, LoginSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from .models import CustomUser, ClientProfile

# Create your views here.

class ClientRegisterView(generics.GenericAPIView):
    serializer_class = ClientRegistrationSerializer
    
    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        user_data = serializer.data
        
        user = CustomUser.objects.get(email=user_data['email'])
        
        #token = RefreshToken.for_user(user).access_token
        
        return Response(user_data, status=status.HTTP_201_CREATED)
    
    
class LoginAPIView(generics.GenericAPIView):
    
    serializer_class = LoginSerializer
    
    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)