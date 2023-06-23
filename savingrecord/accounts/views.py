from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.models import User, auth
from .forms import EmailForm, UserUpdateForm, ProfileUpdateForm
from .forms import ContactForm
from django.contrib.auth.decorators import login_required

from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib.sites.models import Site
from django.contrib.auth import get_user_model


def contact_us(request):

	if request.method == "POST":
		form = ContactForm(request.POST)
		if forms.is_valid():
			name = form.cleaned_data['name']
			email = form.cleaned_data["email"]
			subject = form.cleaned_data["subject"]
			message = form.cleaned_data["message"]

			email_message = f"Name: {name}\nEmail: {email}\nSubject: {subject}\n\n{message}"
	else:
		form = ContactForm()
		

	return render(request, "accounts/pages-contact.html", {})

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
			elif User.objects.filter(email=email).exists():
				messages.info(request, "Email already registed")
				return redirect("register")
			else:
				user = User.objects.create_user(first_name=first_name,
				last_name=last_name, username=username, 
			        email=email, password=password1)
				user.save()
				return redirect("savings")
		elif len(password1) < 8:
			messages.info(request, "The Password Must be 8 or more characters!")
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


def reset_password_request_view(request):

	if request.method == "POST":
		form = EmailForm(request.POST)
		if form.is_valid():
			email = form.cleaned_data["email"]
			try:
				user = User.objects.get(email=email)
			except User.DoesNotExist:
				messages.error(request, "Invalid email")
				return redirect("forgot_password")
			else:
				token = default_token_generator.make_token(user)
				uid = urlsafe_base64_encode(force_bytes(user.pk))
				#current_site = get_current_site(request) current_site to replace the domain
				#domain = current_site.domain
				domain = "127.0.0.1:8000"
				try:
					site = Site.objects.get(domain=domain)
				except Site.DoesNotExist:
					domain = "127.0.0.1:8000/"
				
				mail_subject = "Reset your password request"
				password_reset_url = f"http:{domain}/accounts/reset-password/confirm/{uid}/{token}/"
				message = render_to_string("email_templates/password_reset_email.html", {
						"user": user,
						"password_reset_url": password_reset_url,
						"username": user.username,
						})
				email_message = EmailMessage(mail_subject, message, "noreply@dennis.com", [email])
				email_message.content_subtype = "html"
				email_message.send(fail_silently = False)
				return redirect("password_confirm_request")
	else:
		form = EmailForm()

	return render(request, "accounts/forgot_password.html", {"form": form,})


User = get_user_model()

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
	template_name = "accounts/password_reset_confirm.html"

#   success_url = reverse_lazy("accounts:login")

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["uidb64"] = self.kwargs["uidb64"]
		context["token"]  = self.kwargs["token"]
		return context

	def get(self, request, uidb64, token, *args, **kwargs):
		try:
			uid = force_str(urlsafe_base64_decode(uidb64))
			user = User.objects.get(pk=uid)
		
		except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
			user = None
		
		if user is not None and default_token_generator.check_token(user, token):
			#Valid token, render password reset form
			return super().get(request, uidb64, token, *args, **kwargs, )
		else:
			#Invalid token redirect to error page/ display error message
			return render(request, "accounts/password_reset_invalid.html")
	
	def post(self, request, *args, **kwargs):
		form = self.get_form()
		if form.is_valid():

			#save the password for the user
			user = form.save(commit=False)
			print(f"this is password chenged {password1}")		
			user.set_password(form.cleaned_data["password1"])
			user.save()
		
			return redirect(self.success_url)
		
		return self.form_invalid(form)



def password_confirm_request(request):

	return render(request, "accounts/password_reset_done.html")


@login_required
def userprofile(request):

	if request.method == "POST":
		u_form = UserUpdateForm(request.POST, instance=request.user)
		p_form = ProfileUpdateForm(request.POST, 
			     request.FILES, instance=request.user.profile)
		
		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()

			messages.success(request, f"Your account has been updated successfully!")
			return redirect("userprofile")

	else:
		u_form = UserUpdateForm(instance=request.user)
		p_form = ProfileUpdateForm(instance=request.user.profile)

	context = {
		"u_form": u_form,
		"p_form": p_form,
	}

	return render(request, "accounts/user_profile.html", context)


def changepassword(request):

	return render(request, "accounts/user_profile.html", {})
