from django.urls import path
from .import views

urlpatterns = [
	path("", views.savings, name="savings"),
	path("bank_account", views.bank_account, name="bank_account"),
    path("accounts-operations", views.accounts_operations, name="accounts_operations"),
    path("withraw", views.withdraw_view, name="withraw"),
    path("deposit", views.deposit_view, name="deposit"),
    path("transfer", views.transfar_view, name="transfer"),
    path("savings-record", views.savings_record, name="savings_record"),
    path("target-saving", views.target_saving, name="target_saving"),
    path("daily-saving", views.dairly_deposit, name="dairly_deposit"),
	path("saving-account", views.saving_account, name="saving_account"),
	path("saving-deposit", views.deposit_saving_account, name="saving_deposit"),
	path("calendar/<int:year>/<int:month>", views.calender_view, name ="calendar_view"),
]
