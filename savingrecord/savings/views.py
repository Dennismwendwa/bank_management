from django.shortcuts import render, redirect
from django.urls import path
from django .contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .classes import make_deposit, make_withdraw, make_transfer, calculate_balance, BankAccount
from .classes import get_transaction_history, get_account_details
from .models import Account, accounts_number, Saving_record, Target_saving_record, Statements
from django.contrib import messages
from django.utils import timezone
from .forms import Saving_RecordForm, Target_SavingForm
from django.core.paginator import Paginator

from packs.quotes import money_quotes

@login_required
def savings(request):

	user = User.objects.get(username=request.user.username)

	acc_detail = get_account_details(user)

	statemest = get_transaction_history(user)
	quote = money_quotes()

	return render(request, "savings/index.html", {
		"user": user,
		"acc_detail": acc_detail,
		"statemest": statemest,
        "quote": quote,
		})

def bank_account(request):

	def get_user():
		user = User.objects.get(username=request.user.username)
		return user

	user =  get_user()    # User.objects.get(username=request.user.username)

	acc_detail = Account.objects.filter(user=user)

	count = acc_detail.count() #= 0 
	
	if request.method == "POST":
		if count < 12:
			
			current_datetime = timezone.now()
			account_balance = int(request.POST["account_balance"])
			account_type = request.POST["account_type"]
			first_name = request.POST["first_name"]
			last_name  = request.POST["last_name"]

			account_number = accounts_number(user.id)
			account_name = f"{user.first_name} {user.last_name}"

			account = Account.objects.create(
					account_number = account_number,		
					account_name = account_name,
					account_balance = account_balance,
					opening_date = current_datetime,
					account_type=account_type,
					first_name = first_name,
					last_name = last_name,
					user = user

				)

			obj = BankAccount()
			## Call the create_acco
			result = obj.create_account(account_number, account_name,
					account_balance, account_type)

		else:
			messages.error(request, "You can Only have a maximum of Three(3) accounts")
			return redirect("bank_account")
		
		messages.success(request, """We have received your request.\
				Account will be created within 24hrs. Thanks.""")
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
			messages.error(request, f"""Insufficient funds, Your Balance\
					is {balance_amount}""")
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
			messages.error(request,  f"""Insufficient funds, Your Balance is\
					{balance_amount}""")
			return redirect("transfer")

		elif status == "failed":
			messages.error(request, "Account Does Not exist. Try again")
			return redirect("transfer")

	return render(request, "savings/transfer.html", {})


def savings_record(request):
	
	user = request.user
	record_data = Saving_record.objects.filter(user=user).order_by("-date_saved")
	total = 0
	for items in record_data:
		total += int(items.amount)

	items_per_page = 3

	page_number = request.GET.get("page")

	paginator = Paginator(record_data, items_per_page)

	page_obj = paginator.get_page(page_number)

	if request.method == "POST":

		form = Saving_RecordForm(request.POST)
		if form.is_valid():
			amount = form.cleaned_data["amount"]
			date_saved = form.cleaned_data["date_saved"]
			account_number = form.cleaned_data["account_number"]

			record = Saving_record.objects.create(user=user, amount=amount, 
					date_saved=date_saved,
				account_number=account_number)
			record.save()

		messages.success(request, "Record successfully saved")
		return redirect("savings_record")
	else:
		form = Saving_RecordForm()

	return render(request, "savings/savings_record.html", {
			"form": form,
			"total": total,
			"page_obj": page_obj,
			})


def target_saving(request):
	
	user = request.user
	target_item = Target_saving_record.objects.filter(user=user)
	
	if request.method == "POST":
		form = Target_SavingForm(request.POST)
		if form.is_valid():
			saving_for = form.cleaned_data["saving_for"]
			target_amount = form.cleaned_data["target_amount"]
			saving_par_time = form.cleaned_data["saving_par_time"]
			start_date = form.cleaned_data["start_date"]
			end_date = form.cleaned_data["end_date"]

			checks = Target_saving_record.objects.filter(user=user)
			if checks.filter(saving_for=saving_for).exists():
				messages.error(request, "Project with that name already exist")
				return redirect("target_saving")

			else:
				target = Target_saving_record.objects.create(user=user, saving_for=saving_for,
						target_amount=target_amount, saving_par_time=saving_par_time,
						start_date=start_date, end_date=end_date)
				target.save()
			messages.info(request, "Your saving target was successfully set.")
			return redirect("target_saving")

	else:
		form = Target_SavingForm()



	return render(request, "savings/target_saving.html", {
			"form": form,
			"target_item": target_item,
			})




def dairly_deposit(request):

	user = request.user
	target_item = Target_saving_record.objects.filter(user=user)

	if request.method == "POST":

		amount = int(request.POST["dairly_deposit"])
		project_name = request.POST["project_name"]

		status = calculate_balance(user, amount, project_name)

		if status == "failed":
			messages.error(request, "Something went wrong! Try again")
			return redirect("target_saving")

		elif status == "no-account":
			messages.error(request, "That project name does not exist")
			return redirect("target_saving")

		elif status == "seccuss":
			messages.success(request, "Your record was successfull saved")
		
		return redirect("target_saving")

	return render(request, "savings/target_saving.html", {
			"target_item": target_item,
	
			})











