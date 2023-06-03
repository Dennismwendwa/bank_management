from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from .forms import EmailForm

from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetConfirmView

# Create your views here.

def register(request):

	if request.method == "POST":
		first_name = request.POST["first_name"]
		last_name  = request.POST["last_name"]
		username   = request.POST["username"]
		email      = request.POST["email"]
		password1  = request.POST["password1"]
		password2  = request.POST["password2"]

		
		if password1 == password2 and len(password1) > 7:
			if User.objects.filter(username=username).exists():
				messages.info(request, "Username Taken")
				return redirect("register")
			else:
				if User.objects.filter(email=email).exists():
					messages.info(request, "Email already registed")
					return redirect("register")
				else:
					user = User.objects.create_user(first_name=first_name,
				     last_name=last_name, username=username, 
			email=email, password=password1)
					user.save()
				return redirect("savings")
		elif len(password1) < 8:
			messages.info(request, "The Password Must be 8 or more charactors!")
			return redirect("register")
		else:
			messages.info(request, "Password not matching")
			return redirect ("register")


	return render(request, "accounts/register.html", {})

def login(request):

	if request.method == "POST":
		username = request.POST["username"]
		password = request.POST["password"]

		

		user = auth.authenticate(username=username, password=password)

		if user is not None:
			auth.login(request, user)
			return redirect("savings")
		else:
			messages.info(request, "Invalid credentials")
			return redirect("login")

	return render(request, "accounts/login.html", {})

def logout(request):
	auth.logout(request)
	return redirect("login")


def forgot_password(request):

	if request.method == "POST":
		form = EmailForm(request.POST)
		if form.is_valid():
			form.send_password_reset_email()
			return render(request, "accounts/password_reset_done.html")
	else:
		form = EmailForm()

	return render(request, "accounts/forget_password.html", {"form": form})


class PasswordResetCornfirmViewCustom(PasswordResetConfirmView):
	form_class = SetPasswordForm
	template_name = "accounts/password_reset_confirm.html"
	post_reset_login = True





























