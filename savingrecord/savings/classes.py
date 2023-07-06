from .models import Account, Target_saving_record, Statements, Saving_account
from .models import Saving_account_statements #Target_saving_record_statements
import uuid
import decimal, calendar
from datetime import datetime
from decimal import Decimal, InvalidOperation
from decimal import Decimal
from django .contrib.auth.models import User
from django.utils import timezone
from packs.enryptAES import decrypt_eas

class BankAccount:

	def __init__(self):
		self.accounts = []

	def create_account(self, account_number, account_name, account_balance, account_type):
		account = Account(
				account_number = account_number,
				account_name = account_name,
				account_balance = account_balance,
				account_type = account_type,
				opening_date = timezone.now(),
				)
		self.accounts.append(account)
		return account

	def print_acc():
		for acc in accounts:
			print()
			print(acc)
			print()
	
	def update_status(self, amount, account_no, transaction_type):
		current_acc = None
		for acc in self.accounts:
			
			if acc.account_number == account_no:
				current_acc = acc
				break
			
			if current_acc is None:
				print("Account to updated status not found")

		if current_acc is None:
			print("Account to update status not found")
			return "Account not found"

		transaction_id = str(uuid.uuid4())
		
		match transaction_type:
			case 'deposit':
				current_acc.account_balance += amount
				current_acc.transaction_history.append({'transaction_id': transaction_id, 
					'type': 'deposit', 'amount': amount})

			case "withdraw":
				current_acc.account_balance -= amount
				current_acc.transaction_history.append({'transaction_id': transaction_id,
					'type': 'withdraw', 'amount': amount})

			case "transfer":
				current_acc.account_balance -= amount
				current_acc.transaction_history.append({'transaction_id': transaction_id,
					'type': 'withdraw', 'amount': amount})


	def print_transaction_history(self):
		transaction = self.transaction_history

def not_negative(amount):
	
	if int(amount) > 0:
		return amount
	else:
		return "negative"

def make_deposit(request, amount, account_no):
	
	transaction_date = timezone.now()
	transaction_type = "deposit"
	account_type = "Simba"
	try:
		
		accounts = Account.objects.filter(user=request.user)
		account = accounts.filter(account_number=account_no).first()
		
		if account:
			try:
				account.account_balance += Decimal(amount)
				amount = Decimal(amount)
			except InvalidOperation as e:
			#except decimal.ConversionSyntax as e:
				print(e)
				return "wrong_type"

			status = not_negative(amount)
			if status == "negative":
				return "negative"

			account.total_deposit += amount
			account.total_trans_amount += amount
			account.save()
			helper_status(amount, account_no, transaction_type)
			register_history(account_no, amount, transaction_type, transaction_date, account_type)
			return "success"
		else:
			return "failid"

	except Account.DoesNotExist:
		return "failed"
	
def make_withdraw(request, amount, account_no):
	
	transaction_date = timezone.now()
	transaction_type = "withdraw"
	account_type = "Simba"
	try:
		amount = Decimal(amount)
	except decimal.InvalidOperation:
		return "wrong_type"

	status = not_negative(amount)
	if status == "negative":
		return "negative"

	try:
		accounts = Account.objects.filter(user=request.user)
		account = accounts.filter(account_number=account_no).first()
	
		if account:
			if amount < account.account_balance:
				account.account_balance -= Decimal(amount)
				account.total_withdraw += Decimal(amount)
				account.total_trans_amount += Decimal(amount)
				account.save()
				helper_status(amount, account_no, transaction_type)
				register_history(account_no, amount, transaction_type, transaction_date, account_type)
				return "success"
			else:
				return "lessamount"
		else:
			return "wrong_acc"
		
	except Account.DoesNotExist:
		return "failed"

def make_transfer(amount, transfer_from_acc, transfer_to_acc):

	current_datetime = timezone.now()
	transaction_type = "transfer"
	account_type = "Simba"
	try:
		amount = Decimal(amount)
	except decimal.InvalidOperation:
		return "wrong_type"

	status = not_negative(amount)
	if status == "negative":
		return "negative"

	try:
		transfer_from = Account.objects.get(account_number=transfer_from_acc)
		transfer_to = Account.objects.get(account_number=transfer_to_acc)
	
		if amount < transfer_from.account_balance:
			transfer_from.account_balance -= amount
			transfer_from.total_transfar += amount
			transfer_from.total_trans_amount += amount
			transfer_to.account_balance += amount
			transfer_from.save()
			transfer_to.save()
			helper_status(amount, transfer_from_acc, transaction_type)
			register_history(transfer_from_acc, amount, transaction_type, current_datetime, account_type)
			return "success"
		else:
			return "lessamount"

	except Account.DoesNotExist :
		return "failed"

def saving_deposit(request, amount, account_no):

	transaction_date = timezone.now()
	transaction_type = "deposit"
	account_type = "Saving"
	try:
		accounts = Saving_account.objects.filter(user=request.user)
		account = accounts.filter(account_number=account_no).first()
		#account = accounts.objects.get(account_number=account_no)
		print(account)
		if account:
			account.account_balance += Decimal(amount)
			account.transaction_count = int(account.transaction_count) + 1
			account.save()
			register_history(account_no, amount, transaction_type, transaction_date, account_type)
			return "success"
		else:
			return "failid"
	except Saving_account.DoesNotExist:
		return "no_account"
	


def helper_status(amount, account_no, transaction_type):
	obj = BankAccount()
	obj.update_status(amount, account_no, transaction_type)


class Target_account_st:
	def __init__(self, account_name, amount_save):
		self.account_name = account_name
		self.amount_save = amount_save

	@classmethod
	def record_keeper(cls, account_name, amount_save):
		return cls(account_name, amount_save)

	def stats(self, account_name, amount_save):
		return f"{self.account_name} {self.amount_save}"


def calculate_balance(user, amount, project_name):

	try:
		projects = Target_saving_record.objects.filter(user=user)
		pro_name = projects.filter(saving_for=project_name).first()

		if pro_name is None:
			return "no-account"


	except Target_saving_record.DoesNotExist:
		return "failed"

	else:
		pro_name.amount_saved = int(pro_name.amount_saved) + amount
		pro_name.balence_amount = int(pro_name.target_amount) - int(pro_name.amount_saved)
		pro_name.progress  = (int(pro_name.amount_saved) / int(pro_name.target_amount)) * 100
		pro_name.save()
#		recording = Target_saving_record_statements(
#		project_name = pro_name,
#		amount_saved = amount,
#		date_saved = timezone.now()
#		)
#		recording.save()
		instance = Target_account_st.record_keeper(project_name, amount)
		return "seccuss"



def register_history(account_number, amount, transaction_type, transaction_date, account_type):
	
	if account_type == "Simba":

		try:
			account = Account.objects.get(account_number=account_number)

		except Account.DoesNotExist:
			return "failed"

		else:
			trans_register = Statements(
				account_number = account,
				transaction_type = transaction_type,
				transaction_date = transaction_date,
				amount = amount
			)
			trans_register.save()

			account.last_transaction_date = trans_register.transaction_date
			account.save()

	elif account_type == "Saving":
		try:
			account = Saving_account.objects.get(account_number=account_number)

		except Saving_account_statements.DoesNotExist:
			return "failed"

		else:
			saving_register = Saving_account_statements(
				account_number = account,
				transaction_type = transaction_type,
				amount = amount,
				transaction_date = transaction_date
			)
			saving_register.save()

			account.last_transaction_date = saving_register.transaction_date
			account.save()


def get_transaction_history(user):
	accounts = user.account_set.all()#Account.objects.filter(user=user)
	transactions = Statements.objects.filter(account_number__in=accounts).order_by("-transaction_date")

	return transactions

def get_saving_record_history(user):

	accounts = user.saving_account_set.all()
	saving_record = Saving_account_statements.objects.filter(account_number__in=accounts)

	return saving_record

def get_account_details(user):
	
	details = Account.objects.filter(user=user)

	return details

def get_transaction_percentage(user):
	try:	
		accounts = Account.objects.filter(user=user)
		account = accounts.filter().first()

	except Account.DoesNotExist:
		account, percent_withdral, percent_deposit, percent_transfer = 0, 0, 0, 0
		return account, percent_withdral, percent_deposit, percent_transfer
	else:
		if account:
			try:
				percent_withdral = round((account.total_withdraw / account.total_trans_amount) * 100, 1)
			except decimal.InvalidOperation as e:
				percent_withdral = 0

			try:
				percent_deposit = round((account.total_deposit / account.total_trans_amount) * 100, 1)
			except decimal.InvalidOperation as e:
				percent_deposit = 0

			try:
				percent_transfer = round((account.total_transfar / account.total_trans_amount) * 100, 1)
			except decimal.InvalidOperation as e:
				percent_transfer = 0

			try:
				percent_paybill = round((account.total_paybil / account.total_trans_amount) * 100, 1)
			except decimal.InvalidOperation as e:
				percent_paybill = 0
		
			return account.account_number, percent_withdral, percent_deposit, percent_transfer, percent_paybill
		else:
			account, percent_withdral, percent_deposit, percent_transfer, percent_paybill = 0, 0, 0, 0, 0
			return account, percent_withdral, percent_deposit, percent_transfer, percent_paybill


def get_calender():

	current_date = datetime.now()

	current_year = current_date.year
	month = current_date.month
	day = current_date.day

	month_name = calendar.month_name[month]
	cal = calendar.monthcalendar(current_year, month)

	return month_name, current_year, cal, day

