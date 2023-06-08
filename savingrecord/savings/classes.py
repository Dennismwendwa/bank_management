from .models import Account


class BankAccount:

	a = success
	b = failed

	def __init__(self, account_number, account_name, account_balance, account_type, currency)
		self.account_number = account_number
		self.account_name = account_name
		self.account_balance = account_balance
		self.account_type = account_type
		self.currency = currency
		self.transaction_history = []


	def deposit(self, amount):
		self.account_balance += amount
		self.transaction_history.append(f"Deposit: {amount} {self.currency}")
		return a #success


	def withdraw(self, amount):
		if self.account_balance >= amount:
			self.account_balance -= amount
			self.transaction_history.append(f"Withdrawal: {amount} {self.currency}")
			return a #success
		else:
			messages.error(request, "Insufficient funds.")
			return b #failed


	def print_transaction_history(self):
		transaction = self.transaction_history


