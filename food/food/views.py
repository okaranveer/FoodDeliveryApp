from django.http import HttpResponse 		#importing http response module
from django.shortcuts import render

def homepage(request):
	return render(request,'homepage.html')