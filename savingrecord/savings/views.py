
from django.shortcuts import render, redirect
from django.urls import path
from django .contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .classes import make_deposit, make_withdraw
from .models import Account, accounts_number
from django.contrib import messages
from datetime import datetime
#from classes import Account.deposit



# Create your views here.

@login_required
def savings(request):

	user = User.objects.get(username=request.user.username)

	acc_detail = Account.objects.all()[:3]
	print(acc_detail)


	return render(request, "savings/index.html", {
		"user": user,
		"acc_detail": acc_detail,
		})

def bank_account(request):

	user = User.objects.get(username=request.user.username)
	acc_detail = Account.objects.all()
	
	if request.method == "POST":
		if len(acc_detail) < 4:
			
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
			
		else:
			messages.error(request, "You can Only have a maximum of Three(3) accounts")
			return redirect("bank_account")
		
		
		messages.success(request, "We have received your request. Account will be created within 24hrs. Thanks.")
		return redirect("bank_account")
	
	return render(request, "savings/bank_account.html", {})

def accounts_operations(request):

	return render(request, "savings/forms_layout.html", {})

def withdraw_view(request):

	if request.method == "POST":
		withdraw_amount = request.POST["withdraw"]
		account_no = request.POST["account_no"]
		account_name = request.POST["account_name"]

		status = make_withdraw(withdraw_amount, account_no)

		if status == "success":
			messages.success(request, f"You have withdrawn {withdraw_amount}")
			return redirect("withraw")
		
		elif status == "failed":
			messages.error(request, "Account Does Not exist. Try again")
			return redirect("withraw")
		
		elif status == "lessamount":
			accounts = Account.objects.get(account_number=account_no)
			balance_amount = accounts.account_balance
			messages.error(request, f"Insufficient funds, Your Balance is {balance_amount}")
			return redirect("withraw")



	return render(request, "savings/withdraw.html", {})

def deposit_view(request):

	if request.method == "POST":
		deposit_amount = request.POST["deposit"]
		account_no = request.POST["account_no"]
		account_name = request.POST["account_name"]

		account = Account(account_number=account_no, account_name=account_name,
		    )
		status = make_deposit(deposit_amount, account_no)
			
		if status == "success":
			messages.success(request, f"You have deposited {deposit_amount}")
			return redirect("deposit")
			
		elif status == "failid":
			messages.error(request, "Account Does Not exist. Try again")
			return redirect("deposit")


	return render(request, "savings/deposit.html")








