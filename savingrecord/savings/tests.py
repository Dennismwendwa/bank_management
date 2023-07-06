from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Account
from .views import withdraw_view
from .paybills import pay_bills
from decimal import Decimal

class BankAccountViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

    def test_bank_account_view_with_valid_data(self):
        response = self.client.post(reverse('bank_account'), {
            'account_no': '123456789',
            'account_name': 'Test Account',
            'account_balance': 1000,
            'account_type': 'Savings',  # Add account_type field
            'first_name': 'Test',
            'last_name': 'User'
            })

        self.assertEqual(response.status_code, 302)  # Expecting a redirect
        self.assertRedirects(response, reverse('bank_account'))

        response = self.client.get(reverse('bank_account'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Account.objects.count(), 3)

        account = Account.objects.first()
        self.assertEqual(account.account_balance, 1000)
#        self.assertEqual(account.account_type, 'Savings')
        self.assertEqual(account.first_name, 'Savingsf')
        self.assertEqual(account.last_name, 'Savingsl')
    

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.account = Account.objects.create(user=self.user, account_number='1234567890', account_balance=Decimal('1000.00'))
        self.account_to = Account.objects.create(user=self.user, account_number='0987654321', account_balance=Decimal('500.00'))

    def test_pay_bills_function(self):
        amount_to_pay = '200.00'
        account_number = '1234567890'
        account_to_pay_to = '0987654321'
        result = pay_bills(amount_to_pay, account_number, account_to_pay_to, self.user)
        self.assertEqual(result, 'success')

    def test_pay_bills_insufficient_funds(self):
        amount_to_pay = '1500.00'
        account_number = '1234567890'
        account_to_pay_to = '0987654321'
        result = pay_bills(amount_to_pay, account_number, account_to_pay_to, self.user)
        self.assertEqual(result, 'less_amount')

    def test_pay_bills_invalid_amount(self):
        amount_to_pay = 'invalid'
        account_number = '1234567890'
        account_to_pay_to = '0987654321'
        result = pay_bills(amount_to_pay, account_number, account_to_pay_to, self.user)
        self.assertEqual(result, 'wrong_type')


