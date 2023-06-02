from django.shortcuts import render
from django.urls import path

# Create your views here.

def savings(request):

	return render(request, "savings/index.html")
