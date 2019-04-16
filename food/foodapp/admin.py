from django.contrib import admin

# Register your models here.
from foodapp.models import Restaurant, Customer, Meal, Order, OrderDetails


admin.site.register(Restaurant)
admin.site.register(Customer)
# admin.site.register(Driver)
admin.site.register(Meal)
admin.site.register(Order)
admin.site.register(OrderDetails)