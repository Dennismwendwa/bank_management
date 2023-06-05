from django.shortcuts import render
from django.urls import path
from django .contrib.auth.models import User

# Create your views here.

def savings(request):

	user = User.objects.get(username=request.user.username)
	print(user)
	username = user.username
	print(username)

	return render(request, "savings/index.html", {
		"user": user,
		})
