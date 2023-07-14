from savings.models import Account
from django import forms

#for later
class EditUserDataForm(forms.ModelForm):
    class Meta:

        model = Account
        fields = ["account_name",]
