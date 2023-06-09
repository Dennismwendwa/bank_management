from django.db import models
from django.db.models import Max
from datetime import datetime

# Create your models here.
class Account(models.Model):
	account_name = models.CharField(max_length=100)
	account_number = models.CharField(max_length=50, unique=True)
	account_balance = models.DecimalField(max_digits=12, decimal_places=4)
	account_type = models.CharField(max_length=50)
	account_status = models.CharField(max_length=50, default="active")
	opening_date = models.DateTimeField(null=True)
	last_transaction_date = models.DateTimeField(null=True)
	first_name = models.CharField(max_length=100, default="Savingsf")
	last_name  = models.CharField(max_length=100, default="Savingsl")



	def __str__ (self):
		return f"{self.account_name} - {self.account_number} - {self.account_status}"
	

def accounts_number():
	part1 = "ACCT"
	
	max_account_number = Account.objects.aggregate(Max("account_number"))["account_number__max"]

	if max_account_number:
		start = int(max_account_number[4:])
	else:
		start = 0

	start += 1
	account_nu = f"{start:04d}"

	return f"{part1}{account_nu}"
