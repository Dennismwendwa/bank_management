from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from .forms import EmailForm

from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponseRedirect
from django.conf import settings


# Create your views here.
def home(request):

	return render(request, "savings/indexx.html", {})

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
			email = form.cleaned_data["email"]
			form.send_password_reset_email()
			return render(request, "accounts/password_reset_done.html")
	else:
		form = EmailForm()

	return render(request, "accounts/forgot_password.html", {"form": form})

class CustomPasswordResetView(PasswordResetView):
	email_template_name = "email_templates/password_reset_email.html"

	def send_mail(self, subject_template_name, email_template_name,
			context, from_email, to_email, html_email_template_name=None):
		subject = render_to_string(subject_template_name, context)


		#remove any line breaks from the subject
		subject = "".join(subject.splitlines())
		body = render_to_string(email_template_name, context)
		print(from_email)
		print(to_email)

		send_mail(print(subject), subject, body, from_email, [to_email], html_message=body)



class CustomPasswordResetConfirmView(PasswordResetConfirmView):
	template_name = "accounts/password_reset_confirm.html"

	def form_valid(self, form):
		uidb64 = self.kwargs["uidb64"]
		token  = self.kwargs["token"]

		try:
			uid = force_str(urlsafe_base64_decode(uidb64))
			user = UserModel._default_manager.get(pk=uid)
		except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
			user = None

		if user is not None and default_token_generator.check_tokrn(user, token):
			newpassword = form.cleaned_data["newpassword1"]
			user.set_password(newpassword)
			user.save()

			return HttpResponseRedirect(reverse("password_reset_complete"))

		return self.render_to_response(self.get_context_data(form=form))



def userprofile(request):

	return render(request, "accounts/user_profile.html", {})