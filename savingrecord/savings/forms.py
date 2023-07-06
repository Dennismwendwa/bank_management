from django import forms
from .models import Account, Saving_record, Target_saving_record, Agents

class BankAccountForm(forms.ModelForm):
    class Meta:

        model = Account
        fields = ["account_balance", "account_type", 
                "first_name", "last_name"]


class Saving_RecordForm(forms.ModelForm):
    class Meta:

        model = Saving_record
        fields = ["amount", "date_saved", "account_number"]


class Target_SavingForm(forms.ModelForm):
    class Meta:

        model = Target_saving_record
        fields = ["saving_for", "target_amount", "saving_par_time", 
                "start_date", "end_date"]


class AgentForm(forms.ModelForm):
    class Meta:

        model = Agents
        fields = ["first_name", "last_name", "id_number", "dealer_id", 
                "contact_number", "address"]


