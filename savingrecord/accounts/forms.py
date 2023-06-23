from django import forms
from django.contrib.auth.forms import PasswordResetForm
from .models import Profile
from django.contrib.auth.models import User

class EmailForm(forms.Form):
	email = forms.EmailField()

	def send_password_reset_email(self):
		email = self.cleaned_data["email"]
		form = PasswordResetForm(data={"email": email})
		if form.is_valid():
			form.save()

#User update form
class UserUpdateForm(forms.ModelForm):
	email = forms.EmailField()
	first_name = forms.CharField(max_length=100)
	last_name  = forms.CharField(max_length=100)

	class Meta:
		model = User
		#not updating username currently
		fields = ["email", "first_name", "last_name"]

#User profile update form
class ProfileUpdateForm(forms.ModelForm):
	class Meta:

		model = Profile
		fields = ["image", "about", "company", "job", "country",
	   "address", "phone", "twitter_profile", "facebook_profile",
	   "instagram_profile", "linkedin_profile"
	   ]


#cantant form
class ContactForm(forms.Form):
	name = forms.CharField(max_length=100)
	email = forms.EmailField()
	subject = forms.CharField(max_length=100)
	message = forms.CharField(widget=forms.Textarea)
