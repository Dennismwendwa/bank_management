from django.shortcuts import render, redirect
from django.urls import path
from django .contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import BankAccountForm
from .models import Account, accounts_number
from django.contrib import messages
from datetime import datetime



# Create your views here.

@login_required
def savings(request):

	user = User.objects.get(username=request.user.username)

	acc_detail = Account.objects.all()[:1]
	print(acc_detail)


	return render(request, "savings/index.html", {
		"user": user,
		"acc_detail": acc_detail,
		})

def bank_account(request):

	user = User.objects.get(username=request.user.username)
	
	if request.method == "POST":
		current_datetime = datetime.now()
		formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")

		account_balance = request.POST["account_balance"]
		account_type = request.POST["account_type"]
		first_name = request.POST["first_name"]
		last_name  = request.POST["last_name"]
		
		account = Account.objects.create(
					account_number= accounts_number(),
					account_name = f"{user.first_name} {user.last_name}",
					account_balance= int(account_balance),
					opening_date = formatted_datetime,
					account_type=account_type,
					first_name = first_name,
					last_name = last_name,

				)
		
		
		messages.success(request, "We have received your request. Account will be created within 24hrs. Thanks.")
		return redirect("bank_account")
	
		


	return render(request, "savings/bank_account.html", {})

def accounts_operations(request):

	return render(request, "savings/forms_layout.html", {})
