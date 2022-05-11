from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django_countries.fields import CountryField
from django.db.models.signals import post_save
from django.dispatch import receiver


Category_choice = (
    ('Men', 'Men'),
    ('Women', 'Women'),
    ('Children', 'Children'),
)
Label_choice = (
    ('primary', 'primary'),
    ('secondary', 'secondary'),
    ('danger', 'danger'),
)


class Userprofile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE
    )
    stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)
    one_click_purchasing = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Item(models.Model):
    title = models.CharField(max_length=100)
    category = models.CharField(choices=Category_choice, max_length=200)
    slug = models.SlugField()
    image = models.ImageField()
    url = models.URLField()
    ShowCastToCustomers = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,blank=True,null=True)

    class Meta:
        abstract = True


class MpesaPayment(BaseModel):
    transaction_id = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    transaction_type = models.TextField()
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.TextField()

    class Meta:
        verbose_name = 'Mpesa Payment'
        verbose_name_plural = 'Mpesa Payments'

    def __str__(self):
        return self.first_name


class Wallet(models.Model):
    user_name = models.CharField(max_length=100, blank=True, null=True)
    available_balance = models.DecimalField(('available_balance'), max_digits=6, decimal_places=2, default=0)
    date_modified = models.DateTimeField(auto_now=True,blank=True ,null=True)
    date_created = models.DateTimeField(auto_now=False, auto_now_add=True, null=True)

    def __str__(self):
        return self.user_name

