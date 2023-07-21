import unittest
from django.test import TestCase, Client
from decimal import Decimal
from accounts.models import User
from django.utils import timezone

from .views import admin_deposit_simba
from savings.models import Account
from django.utils import timezone


class TestAdminDeposit_simbaView(unittest.TestCase):
    def setUp(self):

        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="12345678")
        self.client = Client()
        self.client.login(username="testuser", password="12345678")

    def test_valid_deposit(self):

        initial_balance = Decimal("1000.00")
        deposit_amount = Decimal("500.00")
        account_number = "ACC1234"

        account = Account.objects.create(
            user=self.user,
            account_number=account_number,
            account_balance=initial_balance,
        )

        response = self.client.post("/userdata/admin_deposit/", data={
            'deposit_amount': deposit_amount,
            'account': account_number,
            'user_id': self.user.id,
            })

        print("This test is not complete")

  #      self.assertEqual(response.status_code, 302)
        account.refresh_from_db()
        newaccount = Account.objects.get(account_number="ACC1234")
        newbalance = newaccount.account_balance
        expected_balance = initial_balance + deposit_amount
#        self.assertEqual(newbalance, expected_balance)


