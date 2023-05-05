from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, ClientProfile, PharmacistProfile


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