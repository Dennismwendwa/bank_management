from django import forms
from django.contrib.auth.forms import PasswordResetForm

class EmailForm(forms.Form):
	email = forms.EmailField()

	def send_password_reset_email(self):
		email = self.cleaned_data["email"]
		PasswordResetForm(data={"email": email}).save(
				request=None, 
				use_https=False,
				form_email=None, 
				email_template_name="accounts/password_reset_email.html", 
				subject_template_name="accounts/password_reset_subject.txt"
				)
