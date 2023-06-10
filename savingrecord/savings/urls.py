from django.urls import path
from . import views

urlpatterns = [
	path("", views.savings, name="savings"),
	path("bank_account", views.bank_account, name="bank_account"),
    path("accounts-operations", views.accounts_operations, name="accounts_operations"),
    path("withraw", views.withdraw_view, name="withraw"),
    path("deposit", views.deposit_view, name="deposit"),
    path("transfer", views.transfar_view, name="transfer"),
]
