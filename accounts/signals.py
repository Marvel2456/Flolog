from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, Client, Pharmacist
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail
from django.urls import reverse
from .utils import generate_referral_code
import threading


# def send_email_background(subject, message, from_email, recipient_list):
#     def send_email():
#         send_mail(subject, message, from_email, recipient_list)

#     thread = threading.Thread(target=send_email)
#     thread.start()


@receiver(post_save, sender=CustomUser)
def create_portfolio(sender, instance, created, **kwargs):
    client = CustomUser.objects.filter(is_client=True)
    if created:
        
        user = instance
        if instance.is_client:
            client = Client.objects.create(
                user = user,
                email = user.email,
                first_name = user.first_name,
                last_name = user.last_name,
                phone_number = user.phone_number,
                country = user.country,
                state = user.state,
                city = user.city,
            )
            

@receiver(post_save, sender=Client)
def update_user(sender, instance, created, **kwargs):
    client = instance
    user = client.user

    if created == False:
        user.email = client.email
        user.first_name = client.first_name
        user.last_name = client.last_name
        user.phone_number = client.phone_number
        user.country = client.country
        user.state = client.state
        user.city = client.city
        user.save()



@receiver(post_save, sender=CustomUser)
def create_pharma_portfolio(sender, instance, created, **kwargs):

    if created:
        user = instance
        if instance.is_pharmacist:
            pharmacist = Pharmacist.objects.create(
                user = user,
                email = user.email,
                first_name = user.first_name,
                last_name = user.last_name,
                phone_number = user.phone_number,
                referral_code = generate_referral_code()
            )

@receiver(post_save, sender=Pharmacist)
def update_pharma_user(sender, instance, created, **kwargs):
    pharmacist = instance
    user = pharmacist.user

    if created == False:
        user.email = pharmacist.email
        user.first_name = pharmacist.first_name
        user.last_name = pharmacist.last_name
        user.phone_number = pharmacist.phone_number
        user.save()


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        "[email protected]",
        # to:
        [reset_password_token.user.email]
    )