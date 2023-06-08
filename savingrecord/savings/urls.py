from django.urls import path
from . import views

urlpatterns = [
	path("", views.savings, name="savings"),
	path("bank_account", views.bank_account, name="bank_account")
]
