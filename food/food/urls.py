"""food URL Configuration
 
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
# from . import views
from foodapp import views as views
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views



 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),

    
    # Restaurant
    path('restaurant/', views.restaurant_home, name = 'restaurant-home'),

    path('restaurant/sign-in/', views.restaurant_sign_in, name = 'restaurant-sign-in'),

    path('restaurant/sign-out', views.restraunt_signout, name='restaurant-signout'),

    path('restaurant/sign-up', views.restaurant_sign_up, name = 'restaurant-sign-up'),
    
    path('restaurant/account/', views.restaurant_account, name = 'restaurant-account'),
    path('restaurant/meal/', views.restaurant_meal, name = 'restaurant-meal'),
    path('restaurant/meal/add/', views.restaurant_add_meal, name = 'restaurant-add-meal'),
    path('restaurant/meal/edit/<meal_id>/', views.restaurant_edit_meal, name = 'restaurant-edit-meal'),
    path('restaurant/order/', views.restaurant_order, name = 'restaurant-order'),
    path('restaurant/customer/<restaurant_id>/', views.restaurant_customer, name = 'restaurant-customer'),
    path('restaurant/report/', views.restaurant_report, name = 'restaurant-report'),



    ###########
     #CUSTOMER
    ###########
    path('customer/signup/',views.customer_signup, name="customer_signup"),

    path('customer/login/',views.customer_login, name="customer_login"),

    path('customer/logout/', views.customer_logout, name='customer_logout'),

    path('customer/restaurants/',views.customer_get_restaurants, name='get-restaurants'),
    path('customer/meals/<restaurant_id>/',views.customer_get_meals, name="get-meals"),
    path('customer/order/add/',views.customer_add_order, name="add-order"),
    path('customer/account/' ,views.customer_account, name="customer-account"),
    # path('customer/order/latest/',views.customer_get_latest_order),
    # path('customer/order/history', views.customer_order_history, name="customer_order_history")


    

]

urlpatterns+= staticfiles_urlpatterns()

urlpatterns+= static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)