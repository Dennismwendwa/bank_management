from django.shortcuts import render
from django.urls import path
from django .contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import BankAccountForm
from .models import Account


# Create your views here.

@login_required
def savings(request):

	user = User.objects.get(username=request.user.username)
	print(user)
	username = user.username
	print(username)

	return render(request, "savings/index.html", {
		"user": user,
		})

def bank_account(request):

	if request.method == "POST":
		f_account_name = request.POST["account_name"]
		f_opening_date = request.Post["opening_date"]
		f_account_balance = request.POST["account_balance"]
		f_account_type = request.POST["account_type"]
		f_first_name = request.POST["first_name"]
		f_last_name  = request.POST["last_name"]

		account = Account.objects.create(
				account_number='1234567890',
				account_name='John Doe',
				account_balance= int(f_account_balance),
				opening_date = f_opening_date,
				account_type=f_account_type,
				first_name = f_first_name,
				last_name = f_last_name,

				)


	return render(request, "savings/bank_account.html", {})
