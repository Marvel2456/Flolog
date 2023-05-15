from django.shortcuts import render
from .serializers import *
from rest_framework import generics, status
from rest_framework.response import Response
from .models import CustomUser, ClientProfile, PharmacistProfile, Plan
from rest_framework.decorators import api_view, permission_classes
from .emails import send_otp
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
import uuid

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
    

# Pharmacist registration view 
class PharmacistRegisterView(generics.GenericAPIView):
    # permission_classes = [IsAdminUser]
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

    

@api_view(['GET'])
@permission_classes([IsAdminUser])
def client_profile_list(request):
    profile = ClientProfile.objects.all()
    serializer = ClientSerializer(profile, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def pharmacist_profile_list(request):
    profile = PharmacistProfile.objects.all()
    serializer = PharmacistProfileSerializer(profile, many=True)
    return Response(serializer.data)


class ClientDetailView(APIView):
    permission_classes = [IsAdminUser]
    """
    Retrieve, update or delete a client instance.
    """
    def get_object(self, uuid):
        try:
            return ClientProfile.objects.get(id=uuid)
        except ClientProfile.DoesNotExist:
            raise Http404

    def get(self, request, uuid, format=None):
        client = self.get_object(uuid)
        serializer = ClientSerializer(client)
        return Response(serializer.data)

    def put(self, request, uuid, format=None):
        client = self.get_object(uuid)
        serializer = ClientSerializer(client, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, uuid, format=None):
        client = self.get_object(uuid)
        client.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ClientUpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        client_profile = ClientProfile.objects.get(user=request.user)
        serializer = ClientProfileSerializer(client_profile)
        return Response(serializer.data)

    def put(self, request, format=None):
        client_profile = ClientProfile.objects.get(user=request.user)
        serializer = ClientProfileSerializer(client_profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class PharmaUpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        pharma_profile = PharmacistProfile.objects.get(user=request.user)
        serializer = PharmacistProfileSerializer(pharma_profile)
        return Response(serializer.data)

    def put(self, request, format=None):
        pharma_profile = PharmacistProfile.objects.get(user=request.user)
        serializer = PharmacistProfileSerializer(pharma_profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = CustomUser
    permission_classes = [IsAuthenticated]

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class PharmacistDetailView(APIView):
    permission_classes = [IsAdminUser]
    """
    Retrieve, update or delete a client instance.
    """
    def get_object(self, uuid):
        try:
            return PharmacistProfile.objects.get(id=uuid)
        except PharmacistProfile.DoesNotExist:
            raise Http404

    def get(self, request, uuid, format=None):
        client = self.get_object(uuid)
        serializer = PharmacistProfileSerializer(client)
        return Response(serializer.data)

    def put(self, request, uuid, format=None):
        client = self.get_object(uuid)
        serializer = PharmacistProfileSerializer(client, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, uuid, format=None):
        client = self.get_object(uuid)
        client.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
