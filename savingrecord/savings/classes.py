from .models import Account
import uuid
from decimal import Decimal

class BankAccount:

	def __init__(self, account_number, account_name, 
	      account_balance, account_type, currency):
		
		self.account_number = account_number
		self.account_name = account_name
		self.account_balance = account_balance
		self.account_type = account_type
		#self.currency = currency
		self.transaction_history = []
	
	@classmethod
	def create_account(crl, account_number, account_name, account_balance, 
			account_type, transaction_history):
		return "success"
	
	def update_status(self, amount, account_no):
		transaction_id = str(uuid.uuid4())
		self.account_balance += amount
		self.transaction_history.append({'transaction_id': transaction_id, 'type': 'deposit', 'amount': amount})
		return "success"


	

def make_deposit(amount, account_no):
	try:
		accounts = Account.objects.get(account_number=account_no)
		accounts.account_balance += Decimal(amount)
		accounts.save()

		#bank_account = BankAccount()
		#bank_account.update_status(amount, account_no)
		return "success"

	except Account.DoesNotExist:
		return "failed"
	
def make_withdraw(amount, account_no):
	try:
		accounts = Account.objects.get(account_number=account_no)

		if Decimal(amount) < accounts.account_balance:
			accounts.account_balance -= Decimal(amount)
			accounts.save()
			return "success"
		else:
			return "lessamount"

	except Account.DoesNotExist:
		return "failed"



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


