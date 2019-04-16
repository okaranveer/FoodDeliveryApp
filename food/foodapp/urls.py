from django.urls import path
from . import views

app_name = 'foodapp'

urlpatterns = [
	path('customer/signup/',views.signup_view, name="signup"),
	path('customer/login/',views.login_view, name="login"),
	path('customer/logout/',views.logout_view, name="logout"),
]

