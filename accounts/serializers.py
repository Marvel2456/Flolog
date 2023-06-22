from rest_framework import serializers
from .models import CustomUser, Client, Pharmacist, Plan, Activity, CareForm
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from .utils import generate_referral_code



class ClientRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=250)
    first_name = serializers.CharField(max_length=250)
    last_name = serializers.CharField(max_length=250)
    phone_number = serializers.CharField(max_length=100)
    country = serializers.CharField(max_length=250)
    state = serializers.CharField(max_length=250)
    city = serializers.CharField(max_length=250)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'phone_number', 'country', 'state', 'city', 'password',]
        extra_kwargs = {
            'password': {'write_only':True}   
        }

    # Validating the email and phone number

    def validate(self, args):
        email = args.get('email', None)
        first_name = args.get('first_name', None)
        last_name = args.get('last_name', None)
        phone_number = args.get('phone_number',None)
        country = args.get('country', None)
        state = args.get('state', None)
        city = args.get('city', None)
        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email':('email already exists')})
        if CustomUser.objects.filter(phone_number=phone_number).exists():
            raise serializers.ValidationError({'phone_number':('this phone number already exists')})

        return super().validate(args)
    
    def create(self, validated_data):
        validated_data['is_client'] = True
        return CustomUser.objects.create_user(**validated_data)
    

class ClientVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()
    

#  Pharmacist registration serializer   

class PharmacistRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=250)
    phone_number = serializers.CharField(max_length=100)
    # referral_code = serializers.CharField(max_length=10)

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'phone_number', 'password',]
        extra_kwargs = {
            'password': {'write_only':True}   
        }

    # Validating the email and phone number

    def validate(self, args):
        email = args.get('email', None)
        phone_number = args.get('phone_number',None)
        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email':('email already exists')})
        if CustomUser.objects.filter(phone_number=phone_number).exists():
            raise serializers.ValidationError({'phone_number':('this phone number already exists')})
        
        return super().validate(args)
    
    def create(self, validated_data):
        validated_data['is_pharmacist'] = True

        return CustomUser.objects.create_user(**validated_data)
    

# Login serializer

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=250, min_length=6)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    tokens = serializers.CharField(read_only=True)
    is_client = serializers.BooleanField(read_only=True)
    is_pharmacist = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'tokens', 'is_client', 'is_pharmacist']
        
    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        
        user = auth.authenticate(email=email, password=password)
        
        if not user:
          raise AuthenticationFailed('Invalid credentials, try agian') 
        if not user.is_active:
            raise AuthenticationFailed('Your account has been disabled, contact Admin')
        
        return {
            'email': user.email,
            'tokens' : user.tokens,
            'is_client' : user.is_client,
            'is_pharmacist' :user.is_pharmacist
        }
    
    
class ClientListSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Client
        fields = '__all__'

class PharmacistListSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Pharmacist
        fields = '__all__'


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['email', 'first_name', 'last_name', 'phone_number', 'coin', 'country', 'state', 'city',]

class PharmacistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pharmacist
        fields = ['email', 'first_name', 'last_name', 'phone_number', 'balance', 'referral_code',]

class GoLiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pharmacist
        fields = ['is_live',]

class ChangePasswordSerializer(serializers.Serializer):
    model = CustomUser

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'


class AdminActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'
        

class CareFormSerializer(serializers.ModelSerializer):
    pharmacist = PharmacistSerializer(many=False, read_only=True)
    class Meta:
        model = CareForm
        fields = '__all__'
