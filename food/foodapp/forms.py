from django import forms
from django.contrib.auth.models import User
from foodapp.models import Restaurant,Meal

class UserForm(forms.ModelForm):
    
    email=forms.CharField(max_length=100, required=True)
    password=forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model=User
        fields=("email", "password", "first_name", "last_name", "username")

class UserFormForEdit(forms.ModelForm):
    email = forms.CharField(max_length=100, required=True)
    phone = forms.CharField(max_length=100, required=True)
    address = forms.CharField(max_length=100, required=True)


    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "phone", "address")

class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ("name", "phone", "address")

class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        exclude = ("restaurant",)

