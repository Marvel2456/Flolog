from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, ClientProfile, PharmacistProfile
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail
from django.urls import reverse


@receiver(post_save, sender=CustomUser)
def create_portfolio(sender, instance, created, **kwargs):

    if created and CustomUser.objects.filter(is_client=True):
        user = instance
        profile = ClientProfile.objects.create(
            user = user,
            email = user.email,
            first_name = user.first_name,
            last_name = user.last_name,
            phone_number = user.phone_number,
            country = user.country,
            state = user.state,
            city = user.city,
        )

@receiver(post_save, sender=ClientProfile)
def update_user(sender, instance, created, **kwargs):
    client_profile = instance
    user = client_profile.user

    if created == False:
        user.email = client_profile.email
        user.first_name = client_profile.first_name
        user.last_name = client_profile.last_name
        user.phone_number = client_profile.phone_number
        user.country = client_profile.country
        user.state = client_profile.state
        user.city = client_profile.city
        user.save()



@receiver(post_save, sender=CustomUser)
def create_pharma_portfolio(sender, instance, created, **kwargs):

    if created and CustomUser.objects.filter(is_pharmacist=True):
        user = instance
        profile = PharmacistProfile.objects.create(
            user = user,
            email = user.email,
            first_name = user.first_name,
            last_name = user.last_name,
            phone_number = user.phone_number,
        )

@receiver(post_save, sender=PharmacistProfile)
def update_pharma_user(sender, instance, created, **kwargs):
    pharma_profile = instance
    user = pharma_profile.user

    if created == False:
        user.email = pharma_profile.email
        user.first_name = pharma_profile.first_name
        user.last_name = pharma_profile.last_name
        user.phone_number = pharma_profile.phone_number
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