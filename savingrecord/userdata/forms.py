from savings.models import Account, Company, BusinessNumber, Agents
from django import forms

#for later
class EditUserDataForm(forms.ModelForm):
    class Meta:

        model = Account
        fields = ["account_name",]

class EditBusinessNumberForm(forms.ModelForm):
    class Meta:

        model = BusinessNumber
        fields = []

class EditCompanyForm(forms.ModelForm):
    class Meta:

        model = Company
        fields = ["name", "email", "contact", "address", "country",
                "approved", "admin_review"
                ]

class EditAgentsForm(forms.ModelForm):
    class Meta:

        model = Agents
        fields = ["first_name", "last_name", "id_number", "dealer_id",
                "contact_number", "address", "status", "agent_number",
                "image"
                ]
