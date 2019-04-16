from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from foodapp.forms import UserForm, RestaurantForm, UserFormForEdit, MealForm

from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from foodapp.models import *

from django.db.models import Sum, Count, Case, When
from django.utils import timezone
from django.http import HttpResponse

 
 
# Create your views here.

def home(request):
    return redirect('/customer/login')

def customer_login(request):
	if request.method == 'POST':
		form = AuthenticationForm(data=request.POST)
		if form.is_valid():
			#login the user
			user = form.get_user()
			login(request,user)
			if 'next' in request.POST:
				return redirect(request.POST.get('next'))
			else:
				return redirect('get-restaurants')
	else:
		form = AuthenticationForm()
	return render(request, 'customer/login.html', {'form' : form})
#request variable is accessible inside any template


def customer_logout(request):
	logout(request)
	return redirect('/customer/login/')

def customer_signup(request):
	# if request.method == 'POST':
	# 	form = UserCreationForm(request.POST)
	# 	if form.is_valid():
	# 		user = form.save() #if form is valid we save the user
	# 		# log the user in
	# 		login(request,user)
	# 		return redirect('get-restaurants')         						
	# 	form = UserCreationForm()
	# return render(request,'customer/signup.html', {'form' : form})

    user_form = UserForm()

    if request.method == "POST":
        user_form = UserForm(request.POST)

        if user_form.is_valid():
            new_user = User.objects.create_user(**user_form.cleaned_data)
            new_user.save()

            login(request, authenticate(
                username = user_form.cleaned_data["username"],
                password = user_form.cleaned_data["password"]
            ))
            customer = Customer(user=new_user)
            customer.save()
            return redirect('get-restaurants')

    return render(request, "customer/sign_up.html", {"user_form": user_form})


##############
#restaurant
##############

@login_required(login_url='/restaurant/sign-in/')
def restaurant_home(request):
    return redirect('restaurant-order')

# @login_required(login_url='/restaurant/sign-in/')
def restaurant_account(request):
    user_form = UserFormForEdit(instance = request.user)
    restaurant_form = RestaurantForm(instance = request.user.restaurant)

    if request.method == "POST":
        user_form = UserFormForEdit(request.POST, instance = request.user)
        restaurant_form = RestaurantForm(request.POST, request.FILES, instance = request.user.restaurant)

        if user_form.is_valid() and restaurant_form.is_valid():
            user_form.save()
            restaurant_form.save()

    return render(request, 'restaurant/account.html', {
        "user_form": user_form,
        "restaurant_form": restaurant_form
    })

@login_required(login_url='/restaurant/sign-in/')
def restaurant_meal(request):
    meals = Meal.objects.filter(restaurant = request.user.restaurant).order_by("-id")
    return render(request, 'restaurant/meal.html', {"meals": meals})


@login_required(login_url='/restaurant/sign-in/')
def restaurant_add_meal(request):
    form = MealForm()

    if request.method == "POST":
        form = MealForm(request.POST, request.FILES)

        if form.is_valid():
            meal = form.save(commit=False)
            meal.restaurant = request.user.restaurant
            meal.save()
            return redirect(restaurant_meal)

    return render(request, 'restaurant/add_meal.html', {
        "form": form
    })

 
@login_required(login_url='/restaurant/sign-in/')
def restaurant_edit_meal(request, meal_id):
    form = MealForm(instance = Meal.objects.get(id = meal_id))

    if request.method == "POST":
        form = MealForm(request.POST, request.FILES, instance = Meal.objects.get(id = meal_id))

        if form.is_valid():
            form.save()
            return redirect('restaurant-meal')

    return render(request, 'restaurant/edit_meal.html', {
        "form": form
    })

@login_required(login_url='/restaurant/sign-in/')
def restaurant_order(request):
    if request.method == "POST":
        order = Order.objects.get(id = request.POST["id"], restaurant = request.user.restaurant)

        if order.status == Order.COOKING:
            order.status = Order.DELIVERED
            order.save()

    orders = Order.objects.filter(restaurant = request.user.restaurant).order_by("-id")
    return render(request, 'restaurant/order.html', {"orders": orders})

@login_required(login_url='/restaurant/sign-in/')
def restaurant_customer(request):
    if request.method == "POST":
        customer = Customer.objects.get(id = request.POST["id"], restaurant = request.user.restaurant)

    orders = Order.objects.filter(restaurant = request.user.restaurant).order_by("-id")
    return render(request, 'restaurant/customer.html', {"customers": customers})


def restaurant_sign_up(request):
    user_form = UserForm()
    restaurant_form = RestaurantForm()

    if request.method == "POST":
        user_form = UserForm(request.POST)
        restaurant_form = RestaurantForm(request.POST, request.FILES)

        if user_form.is_valid() and restaurant_form.is_valid():
            new_user = User.objects.create_user(**user_form.cleaned_data)
            new_restaurant = restaurant_form.save(commit=False)
            new_restaurant.user = new_user
            new_restaurant.save()

            login(request, authenticate(
                username = user_form.cleaned_data["username"],
                password = user_form.cleaned_data["password"]
            ))

            return redirect(restaurant_home)

    return render(request, "restaurant/sign_up.html", {"user_form": user_form, "restaurant_form": restaurant_form})
 

@login_required(login_url='/restaurant/sign-in/')
def restaurant_report(request):
    #Calculate revenue and number of orders by current week
    from datetime import datetime, timedelta

    revenue = []
    orders = []

    #Calculate weekdays
    today = datetime.now()
    current_weekdays = [today + timedelta(days = i) for i in range( 0 - today.weekday(), 7- today.weekday())]

    for day in current_weekdays:
        delivered_orders = Order.objects.filter(
            restaurant = request.user.restaurant,
            status = Order.DELIVERED,
            created_at__year = day.year,
            created_at__month = day.month,
            created_at__day = day.day
        )
        revenue.append(sum(order.total for order in delivered_orders))
        orders.append(delivered_orders.count())


    # Top 3 Meals
    top3_meals = Meal.objects.filter(restaurant = request.user.restaurant).annotate(total_order = Sum('orderdetails__quantity')).order_by("-total_order")[:3]

    meal = {
        "labels": [meal.name for meal in top3_meals],
        "data": [meal.total_order or 0 for meal in top3_meals]
    }

    

    return render(request, 'restaurant/report.html', {
        "revenue": revenue,
        "orders": orders,
        "meal": meal,
        
    })
def restraunt_signout(request):
    logout(request)
    return redirect("/restaurant/sign-in")


def restaurant_sign_in(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            #login the user
            user = form.get_user()
            login(request,user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('restaurant-order')
    else:
        form = AuthenticationForm()
    return render(request, 'restaurant/sign_in.html', {'form' : form})


##########
#CUSTOMER
##########

@login_required(login_url='/customer/login/')
def customer_get_restaurants(request):
    restaurants = Restaurant.objects.all().order_by("-id")
    return render(request,'customer/get-restaurants.html' , {"restaurants": restaurants})              


@login_required(login_url='/customer/login/')
def customer_get_meals(request, restaurant_id):
    meals = Meal.objects.filter(restaurant_id = restaurant_id).order_by("-id")
    customer = Customer.objects.all()

    return render(request,'customer/get-meals.html' , {"meals": meals, "customer": customer, "restaurant_id": restaurant_id})

@login_required(login_url='/customer/login/')
def customer_add_order(request):

    if request.method == "POST":
        recieved_order = request.POST['order']
        customer = Customer.objects.get(user = request.user)
        order_total=0
        restaurant_id = request.POST["restaurant_id"]
        #fetch restaurant id

        # check if customer has any orders pending
        # if Order.objects.filter(customer = customer).exclude(status = Order.DELIVERED):
        #     return render(request, 'customer/get-restaurants.html',{"status": "failed", "error": "Your last order must be completed."})

        # get details of next order
        order_details = recieved_order
        order_details = order_details.split(';')
        #print (order_details)
        #print (restaurant_id)
        total = 0
        for meals in order_details:
            if meals is not '':
                sub_order_details = meals.split(',')
                print (sub_order_details)
                meal_id = sub_order_details[0]
                quantity = int(sub_order_details[1])
                meal = Meal.objects.get(id=meal_id)
                price = meal.price
                cost = quantity*price
                total = total+cost
        print (total)
             #order_total += Meal.objects.get(id = meal["meal_id"]).price * meal["quantity"]
        # customer_address= order.customer_set.all()
        # print(customer_address)
        order = Order.objects.create(
            customer = customer,
            restaurant = Restaurant.objects.get(pk=restaurant_id),
            total = total,
            status = Order.COOKING,
            # address = customer_address.address
        )
        total = 0

            #step 2 - create Order Details
        for meal in order_details:
            if meal is not '':
                sub_order_details = meal.split(',')
                meal_id = sub_order_details[0]
                quantity = int(sub_order_details[1])
                meals = Meal.objects.get(id=meal_id)
                price = meals.price
                cost = quantity*price
                total = total+cost
                OrderDetails.objects.create(
                    order = order,
                    meal_id = sub_order_details[0],
                    quantity = int(sub_order_details[1]),
                    sub_total = total
                )
        restaurants = Restaurant.objects.all().order_by("-id")            
        return render(request, 'customer/after_order.html')


def customer_account(request):
    user_form = UserFormForEdit(instance = request.user)

    if request.method == "POST":
        user_form = UserFormForEdit(request.POST, instance = request.user)

        if user_form.is_valid():
            user_form.save()

    return render(request, 'customer/account.html', {"user_form": user_form})






# def customer_order_history(request):
#         orders = Order.objects.filter(order_details = request.user).order_by("-id")
#         return HttpResponse("haa")
#         # return render(request, 'customer/history.html', {"orders": orders})







# if request.method == "POST":
#         order = Order.objects.get(id = request.POST["id"], restaurant = request.user.restaurant)

#         if order.status == Order.COOKING:
#             order.status = Order.DELIVERED
#             order.save()

#     orders = Order.objects.filter(restaurant = request.user.restaurant).order_by("-id")
#     return render(request, 'restaurant/order.html', {"orders": orders})