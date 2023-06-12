from django import forms
from .models import Account, Saving_record

class BankAccountForm(forms.ModelForm):
	class Meta:

		model = Account
		fields = ["account_balance", "account_type", 
		"first_name", "last_name"]


class Saving_RecordForm(forms.ModelForm):
	class Meta:

		model = Saving_record
		fields = ["amount", "date_saved", "account_number"]
