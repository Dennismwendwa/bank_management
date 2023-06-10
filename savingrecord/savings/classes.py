from .models import Account
import uuid
from decimal import Decimal
from django .contrib.auth.models import User

class BankAccount:

	def __init__(self):
		self.accounts = []

	def create_account(self, account_number, account_name, account_balance, account_type):
		account = Account(account_number, account_name, account_balance, account_type)
		self.accounts.append(account)
		print(account_number)
		print(account_name)
		print(account_balance)
		print(account_type)
		print("Account created successfully")
	
	def update_status(self, amount, account_no, transaction_type):

		account = None
		for acc in self.accounts:
			if acc.account_number == account_no:
				account = acc
				break

		if account is None:
			return "Account not found"

		transaction_id = str(uuid.uuid4())

		if transaction_type == 'deposit':
			account.account_balance += amount
			account.transaction_history.append({'transaction_id': transaction_id, 'type': 'deposit', 'amount': amount})
			print(f"transaction_id: {transaction_id}, type: 'deposit', 'amount': {amount}")
	

	def withdraw(self, amount):
		if self.account_balance >= amount:
			self.account_balance -= amount
			self.transaction_history.append(f"Withdrawal: {amount} {self.currency}")
			return "success"
		else:
			#messages.error(request, "Insufficient funds.")
			return "failed"


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
			obj = BankAccount()
			obj.update_status(amount, account_no, transaction_type)
			#BankAccount.update_status(amount, account_no, transaction_type)
			
			return "success"
		else:
			return "failid"

	except Account.DoesNotExist:
		return "failed"
	
def make_withdraw(request, amount, account_no):
	try:
		accounts = Account.objects.filter(user=request.user)
		account = accounts.filter(account_number=account_no).first()

		if account:
			if Decimal(amount) < account.account_balance:
				account.account_balance -= Decimal(amount)
				account.save()
				return "success"
			else:
				return "lessamount"
		else:
			return "wrong_acc"
		
	except Account.DoesNotExist:
		return "failed"

def make_transfer(amount, transfer_from_acc, transfer_to_acc):
	try:
		transfer_from = Account.objects.get(account_number=transfer_from_acc)
		transfer_to = Account.objects.get(account_number=transfer_to_acc)
	
		amount = Decimal(amount)
		if amount < transfer_from.account_balance:
			transfer_from.account_balance -= amount
			transfer_to.account_balance += amount
			transfer_from.save()
			transfer_to.save()
			return "success"
		else:
			return "lessamount"

	except Account.DoesNotExist :
		return "failed"

