from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from rest_framework.authtoken.models import Token
from django.conf import settings

# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token(self,sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)

# Create your models here.
class Restaurant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='restaurant')
    name = models.CharField(max_length=500)
    phone = models.CharField(max_length=500)
    address = models.CharField(max_length=500)
    logo = models.ImageField(upload_to='restaurant_logo/', blank=False)

    def __str__(self):
        return self.name

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer')
    avatar = models.CharField(max_length=500, blank=True, null=True)
    phone = models.CharField(max_length=500, blank=True)
    address = models.CharField(max_length=500, blank=True)
    photo = models.ImageField( upload_to = 'customer_photo/', blank=True)

    def __str__(self):
        return self.user.get_full_name()


class Meal(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=500)
    short_description = models.CharField(max_length=500)
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Order(models.Model):
    COOKING = 1
    READY = 2
    ONTHEWAY = 3
    DELIVERED = 4

    STATUS_CHOICES = (
        (COOKING, "Cooking"),
        (READY, "Ready"),
        (ONTHEWAY, "On the way"),
        (DELIVERED, "Delivered"),
    )
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,default=None)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE,default=None)
    # driver = models.ForeignKey(Driver, blank = True, null = True)
    address = models.CharField(max_length=500)
    total = models.IntegerField()
    status = models.IntegerField(choices = STATUS_CHOICES)
    created_at = models.DateTimeField(default = timezone.now)
    picked_at = models.DateTimeField(blank = True, null = True)

    def __str__(self):
        return str(self.id)


class OrderDetails(models.Model):
    order = models.ForeignKey(Order, related_name='order_details', on_delete=models.CASCADE, default=None)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE,default=None)
    quantity = models.IntegerField()
    sub_total = models.IntegerField()

    def __str__(self):
        return str(self.id)
