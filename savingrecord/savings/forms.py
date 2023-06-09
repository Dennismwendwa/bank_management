from django import forms
from .models import Account

class BankAccountForm(forms.ModelForm):
	class Meta:

		model = Account
		fields = ["account_balance", "account_type", 
		"first_name", "last_name"]
