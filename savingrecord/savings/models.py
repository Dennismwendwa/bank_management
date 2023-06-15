from django.db import models
from django.contrib.auth.models import User
from django.db.models import Max
from datetime import datetime
import random, uuid
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


class Saving_record(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	amount = models.CharField(max_length=100)
	date_saved = models.DateTimeField()
	account_number = models.CharField(max_length=100)

	def __str__ (self):
		return f"{self.user.first_name} - {self.account_number}"


class Target_saving_record(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	saving_for = models.CharField(max_length=100)
	target_amount = models.CharField(max_length=100)
	amount_saved = models.CharField(max_length=100, default=0)
	balence_amount = models.CharField(max_length=100, default=0)
	progress = models.CharField(max_length=100, default=0)
	saving_par_time = models.CharField(max_length=100)
	start_date = models.DateTimeField()
	end_date = models.DateTimeField()

	def __str__(self):
		return f"""{self.user.first_name} {self.user.last_name}\
			- {self.target_amount} - {self.progress} - {self.saving_for}"""


class Statements(models.Model):
	account_number = models.ForeignKey(Account, on_delete=models.CASCADE)
	transaction_type = models.CharField(max_length=100)
	amount = models.DecimalField(max_digits=12, decimal_places=4)
	transaction_date = models.DateTimeField()


	def __str__ (self):
		return f"""{self.account_number.account_number}- {self.transaction_type} - 
		{self.amount} - {self.transaction_date} """
    

def accounts_number(user_id):

	
	string_part = "ACC"

	randd = random.randint(1, 10)
	
	uuid_part = str(uuid.uuid4().hex[:8])
	user_num = str(int(user_id) - sum(ord(char) for char in str(user_id))).replace("-", "")
	user_num = int(user_num)
	user_num = str(user_num - randd)


	bank_account_number = string_part + uuid_part + user_num

	return bank_account_number.upper()


