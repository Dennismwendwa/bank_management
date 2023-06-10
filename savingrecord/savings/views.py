
from django.shortcuts import render, redirect
from django.urls import path
from django .contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .classes import make_deposit, make_withdraw, make_transfer, BankAccount
from .models import Account, accounts_number
from django.contrib import messages
from datetime import datetime

@login_required
def savings(request):

	user = User.objects.get(username=request.user.username)

	acc_detail = Account.objects.filter(user=user)[:6]

	return render(request, "savings/index.html", {
		"user": user,
		"acc_detail": acc_detail,
		})

def bank_account(request):

	def get_user():
		user = User.objects.get(username=request.user.username)
		return user

	user =  get_user()    # User.objects.get(username=request.user.username)

	acc_detail = Account.objects.filter(user=user)

	count = acc_detail.count() #= 0 
	
	if request.method == "POST":
		if count < 7:
			
			current_datetime = datetime.now()
			formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
			account_balance = int(request.POST["account_balance"])
			account_type = request.POST["account_type"]
			first_name = request.POST["first_name"]
			last_name  = request.POST["last_name"]

			acc_num = accounts_number(user.id)
			acc_nam = f"{user.first_name} {user.last_name}"

			account = Account.objects.create(
					account_number = acc_num,
					
					account_name = acc_nam,
					account_balance = account_balance,
					opening_date = formatted_datetime,
					account_type=account_type,
					first_name = first_name,
					last_name = last_name,
					user = user

				)
			obj = BankAccount()
			results = obj.create_account(acc_num, acc_nam, account_balance, account_type)  # Call the create_account() method on the instance
			#obj = BankAccount.create_account(acc_num, acc_nam, account_balance, account_type)

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

		status = make_withdraw(request, withdraw_amount, account_no)

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
		
		elif status == "wrong_acc":
			messages.error(request, "You have enterd wrong Account number. try again!")



	return render(request, "savings/withdraw.html", {})

def deposit_view(request):

	if request.method == "POST":
		deposit_amount = request.POST["deposit"]
		account_no = request.POST["account_no"]
		account_name = request.POST["account_name"]

		status = make_deposit(request, deposit_amount, account_no)
			
		if status == "success":
			messages.success(request, f"You have deposited {deposit_amount}")
			return redirect("deposit")
			
		elif status == "failid":
			messages.error(request, "Account Does Not exist. Try again")
			return redirect("deposit")


	return render(request, "savings/deposit.html")


def transfar_view(request):

	if request.method == "POST":
		transfer_amount = request.POST["deposit"].strip()
		transfer_from = request.POST["transfer_from"].strip()
		transfer_to = request.POST["transfer_to"].strip()
		transfer_to_account_name = request.POST["transfer_to_account_name"].strip()
		transfer_from_account_name = request.POST["transfer_from_account_name"].strip()

		status = make_transfer(transfer_amount, transfer_from, transfer_to)

		if status == "success":
			messages.success(request, f"""You have trensfered {transfer_amount} to\
				account {transfer_to}""")
			return redirect("transfer")

		elif status == "lessamount":
			account_t = Account.objects.get(account_number=transfer_from)
			balance_amount = account_t.account_balance
			messages.error(request,  f"Insufficient funds, Your Balance is {balance_amount}")
			return redirect("transfer")

		elif status == "failed":
			messages.error(request, "Account Does Not exist. Try again")
			return redirect("transfer")

	return render(request, "savings/transfer.html", {})











