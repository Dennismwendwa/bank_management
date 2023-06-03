from django import forms
from django.contrib.auth.forms import PasswordResetForm

class EmailForm(forms.Form):
	email = forms.EmailField()

	def send_password_reset_email(self):
		email = self.cleaned_data["email"]
		form = PasswordResetForm(data={"email": email})
		if form.is_valid():
			form.save()
