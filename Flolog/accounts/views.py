from django.shortcuts import render
from .serializers import *
from rest_framework import generics, status
from rest_framework.response import Response
from .models import CustomUser, ClientProfile, PharmacistProfile, Plan
from rest_framework.decorators import api_view, permission_classes
from .emails import send_otp
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated

# Create your views here.


#  client registration view

class ClientRegisterView(generics.GenericAPIView):
    serializer_class = ClientRegistrationSerializer
    
    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        send_otp(serializer.data['email'])
        
        user_data = serializer.data
        
        user = CustomUser.objects.get(email=user_data['email'])
        
        return Response(user_data, status=status.HTTP_201_CREATED)
    
    
#  Verify the client via OTP

class ClientVerifyView(APIView):
    def post(self, request, format=None):
        serializer = ClientVerifySerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data['email']
            otp = serializer.data['otp']
            
            user = CustomUser.objects.filter(email=email)
            if not user.exists():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
            if user[0].otp != otp:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            user = user.first()    
            user.is_verified = True
            user.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


# Pharmacist registration view

class PharmacistRegisterView(generics.GenericAPIView):
    serializer_class = PharmacistRegistrationSerializer
    
    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        user_data = serializer.data
        
        user = CustomUser.objects.get(email=user_data['email'])
        
        return Response(user_data, status=status.HTTP_201_CREATED)
    
    
class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    
    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def client_profile_list(request):
    profile = ClientProfile.objects.all()
    serializer = ClientSerializer(profile, many=True)
    return Response(serializer.data)


class ClientUpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        client_profile = request.user.client_profile
        serializer = ClientProfileSerializer(client_profile)
        return Response(serializer.data)

    def put(self, request, format=None):
        client_profile = request.user.client_profile
        serializer = ClientProfileSerializer(client_profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class PharmaUpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        pharma_profile = request.user.pharma_profile
        serializer = PharmacistProfileSerializer(pharma_profile)
        return Response(serializer.data)

    def put(self, request, format=None):
        pharma_profile = request.user.pharma_profile
        serializer = PharmacistProfileSerializer(pharma_profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


