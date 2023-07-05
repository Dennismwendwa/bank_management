from django.db import models
from django.contrib.auth.models import User
from django.db.models import Max
from datetime import datetime
import random, uuid
import string
from packs.enryptAES import encrypt


# Create your models here.
class Account(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	account_name = models.CharField(max_length=100)
	account_number = models.CharField(max_length=200, unique=True)
	account_balance = models.DecimalField(max_digits=12, decimal_places=4)
	account_type = models.CharField(max_length=50)
	account_status = models.CharField(max_length=50, default="active")
	opening_date = models.DateTimeField(null=True)
	last_transaction_date = models.DateTimeField(null=True)
	first_name = models.CharField(max_length=100, default="Savingsf")
	last_name  = models.CharField(max_length=100, default="Savingsl")
	total_withdraw = models.DecimalField(max_digits=12, decimal_places=4, default=0)
	total_deposit = models.DecimalField(max_digits=12, decimal_places=4, default=0)
	total_transfar = models.DecimalField(max_digits=12, decimal_places=4, default=0)
	total_paybil = models.DecimalField(max_digits=12, decimal_places=4, default=0)
	total_trans_amount = models.DecimalField(max_digits=12, decimal_places=4, default=0)


	def __str__ (self):
		return f"{self.account_name} - {self.account_number} - {self.account_status}"

	#resetting transactions to zero every month end
	@classmethod
	def reset_transaction_fields(cls):
		today = datetime.date.today()
		first_day_of_month = datetime.date(today.year, today.month, 1)
		last_reset_time = first_day_of_month

		current_time = datetime.date.today()
		elapsed_time = current_time - last_reset_time
		if elapsed_time.days >= 30:
			cls.objects.update(
				total_withdraw = 0,
				total_deposit = 0,
				total_transfar = 0,
				total_trans_amount = 0
			) #Account.reset_transaction_fields()


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

#class Target_saving_record_statements(models.Model):
#	target_saving_record = models.ForeignKey(Target_saving_record, on_delete=models.CASCADE)
#	amount_saved = models.DecimalField(max_digits=12, decimal_places=4)
#	date_saved = models.DateTimeField(null=True)
#
#	def __str__(self):
#		return f"{self.target_saving_record.saving_for} {self.date_saved} {self.amount_saved}"

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

	ciphertext = bank_account_number.upper()

	return ciphertext


class Saving_account(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	account_name = models.CharField(max_length=50, default="saving")
	account_number = models.CharField(max_length=1000, unique=True)
	deposit = models.DecimalField(max_digits=12, decimal_places=4)
	account_balance = models.DecimalField(max_digits=12, decimal_places=4)
	last_transaction_date = models.DateTimeField(null=True)
	account_type = models.CharField(max_length=100)
	transaction_count = models.CharField(max_length=100, default=0)
	opening_date = models.DateTimeField()

	def __str__(self):
		return f"{self.account_number} - {self.account_balance}"


class Saving_account_statements(models.Model):
	account_number = models.ForeignKey(Saving_account, on_delete=models.CASCADE)
	transaction_type = models.CharField(max_length=100)
	amount = models.DecimalField(max_digits=12, decimal_places=4)
	transaction_date = models.DateTimeField()

	def __str__(self):
		return f"""{self.account_number.account_number} - 
		{self.transaction_date} - {self.transaction_type}"""
