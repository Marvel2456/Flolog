from django.core.mail import send_mail
import random
from django.conf import settings
from .models import CustomUser


def send_otp(email):
    subject = 'Account verification email'
    otp = random.randint(10000, 99999)
    message = f'Your OTP is {otp}'
    email_from = settings.DEFAULT_FROM_EMAIL
    send_mail(subject, message, email_from, [email])
    user_obj = CustomUser.objects.get(email=email)
    user_obj.otp = otp
    user_obj.save()