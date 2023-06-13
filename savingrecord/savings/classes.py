from .models import Account, Target_saving_record
import uuid
from decimal import Decimal
from django .contrib.auth.models import User
from django.utils import timezone

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
		print()
		print("list start")
		print(account.account_number)
		print(account.account_name)
		print(account.account_balance)
		print(account.account_type)
		print("list end")
		for acc in self.accounts:
			print(acc)
		print("Account created successfully")
		print()
		return account
	
	def update_status(self, amount, account_no, transaction_type):
		current_acc = None
		for acc in self.accounts:
			print()
			print()
			print(acc)
			if acc.account_number == account_no:
				current_acc = acc
				break
			
			if current_acc is None:
				print("Account to updated status not found")
		print()
		print(self.accounts)
		print(f"Amount: {amount} Account no: {account_no} tran type: {transaction_type}")
		print()

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


def make_deposit(request, amount, account_no):

	transaction_type = "deposit"
	try:
		
		accounts = Account.objects.filter(user=request.user)
		account = accounts.filter(account_number=account_no).first()
		
		if account:
			account.account_balance += Decimal(amount)
			account.save()
			helper_status(amount, account_no, transaction_type)
			return "success"
		else:
			return "failid"

	except Account.DoesNotExist:
		return "failed"
	
def make_withdraw(request, amount, account_no):

	transaction_type = "withdraw"
	try:
		accounts = Account.objects.filter(user=request.user)
		account = accounts.filter(account_number=account_no).first()

		if account:
			if Decimal(amount) < account.account_balance:
				account.account_balance -= Decimal(amount)
				account.save()
				helper_status(amount, account_no, transaction_type)
				
				return "success"
			else:
				return "lessamount"
		else:
			return "wrong_acc"
		
	except Account.DoesNotExist:
		return "failed"

def make_transfer(amount, transfer_from_acc, transfer_to_acc):

	transaction_type = "transfer"
	try:
		transfer_from = Account.objects.get(account_number=transfer_from_acc)
		transfer_to = Account.objects.get(account_number=transfer_to_acc)
	
		amount = Decimal(amount)
		if amount < transfer_from.account_balance:
			transfer_from.account_balance -= amount
			transfer_to.account_balance += amount
			transfer_from.save()
			transfer_to.save()
			helper_status(amount, transfer_from_acc, transaction_type)
			return "success"
		else:
			return "lessamount"

	except Account.DoesNotExist :
		return "failed"

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
		instance = Target_account_st.record_keeper(project_name, amount)
		return "seccuss"





























