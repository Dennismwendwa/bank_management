from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Account
from .views import withdraw_view

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
        self.assertEqual(Account.objects.count(), 1)
        account = Account.objects.first()
        self.assertEqual(account.account_balance, 1000)
        self.assertEqual(account.account_type, 'Savings')
        self.assertEqual(account.first_name, 'Test')
        self.assertEqual(account.last_name, 'User')

