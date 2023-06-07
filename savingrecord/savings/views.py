from django.shortcuts import render
from django.urls import path
from django .contrib.auth.models import User
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required
def savings(request):

	user = User.objects.get(username=request.user.username)
	print(user)
	username = user.username
	print(username)

	return render(request, "savings/index.html", {
		"user": user,
		})
