from django import forms
from .models import Account

class BankAccountForm(forms.ModelForm):
	class Meta:

		model = Account
		fields = ["account_name", "account_type", "opening_date", "first_name", "last_name"]
