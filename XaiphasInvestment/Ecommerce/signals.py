from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import *


# @receiver(post_save, sender=MpesaPayment)
# def create_wallet(sender, instance, created, **kwargs):
#     if created:
#         Wallet.objects.create(
#             user_id=
#         )
#

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
		instance.profile.save()