from django.shortcuts import render, get_object_or_404
from .serializers import *
from rest_framework import generics, status
from rest_framework.response import Response
from .models import CustomUser, Client, Pharmacist, Plan, PaymentHistory, Activity
from rest_framework.decorators import api_view, permission_classes
from .emails import send_otp
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .utils import generate_referral_code
import uuid
from django.conf import settings
import requests
import json
from .utils import log_activity
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


#  client registration view

class ClientRegisterView(generics.GenericAPIView):
    serializer_class = ClientRegistrationSerializer
    
    def post(self, request):
        pharma_uuid = request.session.get('ref_profile')
        print('pharma_uuid', pharma_uuid)
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        if pharma_uuid is not None:
            referred_by_pharma = Pharmacist.objects.get(id=pharma_uuid)
            instance = serializer.save()
            client = CustomUser.objects.get(id=instance.id)
            client_profile = Client.objects.get(user=client)
            client_profile.referred_by = referred_by_pharma
            client_profile.save()

            # Reward the referred_by_pharma with 100 naira
            if referred_by_pharma.balance is not None:
                referred_by_pharma.balance += 100
            else:
                referred_by_pharma.balance = 100
            referred_by_pharma.save()
        else:
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
        email = request.data.get('email')

        user = get_object_or_404(CustomUser, email=email)
        log_activity(user, 'Logged into the application')
        
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
    profile = Client.objects.all()
    serializer = ClientListSerializer(profile, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def pharmacist_profile_list(request):
    profile = Pharmacist.objects.all()
    serializer = PharmacistListSerializer(profile, many=True)
    return Response(serializer.data)


class ClientDetailView(APIView):
    permission_classes = [IsAdminUser]
    """
    Retrieve, update or delete a client instance.
    """
    def get_object(self, uuid):
        try:
            return Client.objects.get(id=uuid)
        except Client.DoesNotExist:
            raise Http404

    def get(self, request, uuid, format=None):
        client = self.get_object(uuid)
        serializer = ClientListSerializer(client)
        return Response(serializer.data)

    def put(self, request, uuid, format=None):
        client = self.get_object(uuid)
        serializer = ClientListSerializer(client, data=request.data)
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
        client = Client.objects.get(user=request.user)
        serializer = ClientSerializer(client)
        log_activity(request.user, 'Viewed Profile')
        return Response(serializer.data)

    def put(self, request, format=None):
        client = Client.objects.get(user=request.user)
        serializer = ClientSerializer(client, data=request.data)
        if serializer.is_valid():
            serializer.save()
            log_activity(request.user, 'Updated Profile')
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class PharmaUpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        pharmacist = Pharmacist.objects.get(user=request.user)
        serializer = PharmacistSerializer(pharmacist)
        log_activity(request.user, 'Viewed Profile')
        return Response(serializer.data)

    def put(self, request, format=None):
        pharmacist = Pharmacist.objects.get(user=request.user)
        serializer = PharmacistSerializer(pharmacist, data=request.data)
        if serializer.is_valid():
            serializer.save()
            log_activity(request.user, 'Updated Profile')
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class GoLiveView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        pharmacist = Pharmacist.objects.get(user=request.user)
        pharmacist.is_live = True
        pharmacist.save()
        serializer = GoLiveSerializer(pharmacist)
        log_activity(request.user, 'Went live')
        return Response(serializer.data)
    

class ReferredClientsListAPIView(generics.ListAPIView):
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        pharmacist = self.request.user
        return Client.objects.filter(referred_by=pharmacist)
    


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
            log_activity(request.user, 'Changed Password')
            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class PharmacistDetailView(APIView):
    permission_classes = [IsAdminUser]
    """
    Retrieve, update or delete a client instance.
    """
    def get_object(self, uuid):
        try:
            return Pharmacist.objects.get(id=uuid)
        except Pharmacist.DoesNotExist:
            raise Http404

    def get(self, request, uuid, format=None):
        pharmacist = self.get_object(uuid)
        serializer = PharmacistSerializer(pharmacist)
        return Response(serializer.data)

    def put(self, request, uuid, format=None):
        pharmacist = self.get_object(uuid)
        serializer = PharmacistSerializer(pharmacist, data=request.data)
        if serializer.is_valid():
            serializer.save()
            log_activity(request.user, f'Edited {pharmacist} profile')
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, uuid, format=None):
        client = self.get_object(uuid)
        client.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class UserActivityView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        activities = Activity.objects.filter(user=request.user)
        serializer = ActivitySerializer(activities, many=True)
        return Response(serializer.data)
    

class AdminUserActivityView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        activities = Activity.objects.all()
        serializer = AdminActivitySerializer(activities, many=True)
        return Response(serializer.data)
    

class CareFormView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        pharmacist = Pharmacist.objects.get(user=request.user)
        care_form = CareForm.objects.filter(pharmacist=pharmacist)
        serializer = CareFormSerializer(care_form, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        care_form = CareForm.objects.all()
        pharmacist = Pharmacist.objects.get(user=request.user)
        serializer = CareFormSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(pharmacist=pharmacist)
            log_activity(request.user, f'created a care form for {care_form.patient}')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class AdminCareFormView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, format=None):
        care_form = CareForm.objects.all()
        serializer = CareFormSerializer(care_form, many=True)
        return Response(serializer.data)
    

class AdminDetailCareformView(APIView):
    permission_classes = [IsAdminUser]
    """
    Retrieve, update or delete a client instance.
    """
    def get_object(self, uuid):
        try:
            return CareForm.objects.get(id=uuid)
        except CareForm.DoesNotExist:
            raise Http404

    def get(self, request, uuid, format=None):
        care_form = self.get_object(uuid)
        serializer = CareFormSerializer(care_form)
        return Response(serializer.data)



    def delete(self, request, uuid, format=None):
        care_form = self.get_object(uuid)
        care_form.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

@csrf_exempt    
@api_view(['POST'])
def make_payment(request):
    plan_id = request.data.get('plan_id')

    try:
        plan = Plan.objects.get(id=plan_id)
    except Plan.DoesNotExist:
        return Response({'error': 'Invalid plan ID'}, status=400)

    amount = int(plan.price * 100)  # Convert price to kobo (Paystack uses kobo as the base unit)
    email = request.user.email

    def initaite_payment(request):
        paystack_url = 'https://api.paystack.co/transaction/initialize'
        headers = {
            'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
            'Content-Type': 'application/json',
        }
        data = {
            'amount': amount,
            'email': email,
            'metadata': {
                'plan_id': str(plan.id),
            },
        }
        response = requests.post(paystack_url, headers=headers, json=data)
        response_data = response.json()


        return Response(response_data)
    initialized = initaite_payment(request)
    print(initialized['data']['authorization_url'])
    amount_new = amount/100
    instance = PaymentHistory.objects.create(client=email, amount=amount_new, plan=plan, paystack_charge_id=initialized['data']['reference'],
                                              paystack_access_code=initialized['data']['access_code'])
    instance.save()
    return Response(status=status.HTTP_200_OK)
    


@csrf_exempt
@api_view(['POST'])
def confirm_payment(request):
    reference = request.data.get('reference')

    pay = PaymentHistory.objects.filter(paystack_charge_id=reference).exists()

    if pay == False:
        print('Error')
    else:
        payment = PaymentHistory.objects.get(paystack_charge_id=reference)

        def verify_payment(request):
            paystack_url = f'https://api.paystack.co/transaction/verify/{reference}'
            headers = {
                'Authorization': f'Bearer {settings.PAYSTACK_SECRET_KEY}',
                'Content-Type': 'application/json',
            }
            data = {
                "reference": payment.paystack_charge_id
            }
            response = requests.get(paystack_url, json=data, headers=headers)
            response_data = response.json()
            return Response(response_data)
        
    initialized = verify_payment(request)
    if initialized['data']['status'] == 'success':
        PaymentHistory.objects.filter(paystack_charge_id=initialized['data']['reference']).update(paid=True)
        owner = Client.objects.get(user=request.user)
        client, created = Client.objects.get_or_create(owner=owner)
        client.coin += int(payment.amount) // 500  # Assuming 1 coin = 500 naira
        client.save()

    return Response(status=status.HTTP_201_CREATED)