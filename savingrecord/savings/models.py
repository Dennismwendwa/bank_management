from django.db import models
from django.contrib.auth.models import User
from django.db.models import Max
from datetime import datetime
import random, re
import string


# Create your models here.
class Account(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
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




def accounts_number(user_id):

	
	part1 = "ACCT"
	
	max_account_number = Account.objects.aggregate(Max("account_number"))["account_number__max"]

	if max_account_number:
		numeric_part = re.search(r"\d+", max_account_number)
		if numeric_part:
			start = int(numeric_part.group()) + 1
		else:
			start = 1
	else:
		start = 1

	account_nu = str(start).zfill(4)
    

	random_letters = "".join(random.choices(string.ascii_uppercase, k=4))

	return f"{part1}{user_id}{random_letters}{account_nu}"
