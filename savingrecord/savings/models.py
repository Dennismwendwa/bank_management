from django.db import models
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
	first_name = models.CharField(max_length=100)
	last_name  = models.CharField(max_length=100)


	def __str__ (self):
		return f"{self.account_name} - {self.account_number} - {self.account_status}"
