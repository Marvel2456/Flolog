from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
import uuid
from rest_framework_simplejwt.tokens import RefreshToken

# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):

        if email is None:
            raise TypeError('Email is required')
        
        email=self.normalize_email(email)
        user = self.model(email=email,  **extra_fields)
        user.set_password(password)
        user.save()
        return user
    

    def create_superuser(self, email, password=None, **extra_fields):
        if password is None:
            raise TypeError('Password is required')
        
        user = self.create_user(email, password=password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=250, unique=True)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    phone_number = models.IntegerField(blank=True, null=True)
    country = models.CharField(max_length=250, blank=True, null=True)
    state = models.CharField(max_length=250, blank=True, null=True)
    city = models.CharField(max_length=250, blank=True, null=True)
    otp = models.CharField(max_length=150, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)
    is_pharmacist = models.BooleanField(default=False)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    USERNAME_FIELD = 'email'

    objects = CustomUserManager()
    
    def __str__(self):
        return self.email
    
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh' : str(refresh),
            'access' : str(refresh.access_token)
        } 
    
#  Client profile.

class Client(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    email = models.EmailField(max_length=250, unique=True)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    phone_number = models.IntegerField(blank=True, null=True)
    coin = models.PositiveIntegerField(default=1, blank=True)
    country = models.CharField(max_length=250, blank=True, null=True)
    state = models.CharField(max_length=250, blank=True, null=True)
    city = models.CharField(max_length=250, blank=True, null=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
 


# Pharmacist profile. 

class Pharmacist(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    email = models.EmailField(max_length=250, unique=True)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    phone_number = models.IntegerField(blank=True, null=True)
    balance = models.DecimalField(max_digits=12, decimal_places=3, blank=True, null=True)
    is_live = models.BooleanField(default=False, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
    

class Wallet(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    owner = models.OneToOneField(Pharmacist, on_delete=models.CASCADE)
    balance = models.DecimalField(decimal_places=3, max_digits=12, default=0, blank=True, null=True)
    
    def __str__(self):
        return self.owner
    


class Plan(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    price = models.DecimalField(max_digits=20, decimal_places=3, blank=True, null=True)
    coin = models.PositiveIntegerField(blank=True, null=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False) 

    def __str__(self):
        return self.name
    
    
#  tell the project manager that all of the medication details should be in one form
#  remember to do signup with google and google recaptcha

    
