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

        # Assert that the response has a success status code (e.g., 200, 302)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('bank_account'))
        self.assertContains(response, 'Bank account created successfully')



    def test_failed_withdrawal_account_not_exist(self):
        response = self.client.post(self.with{
                'withdraw': '500',
                'account_no': '987654321',  # Non-existent account number
                'account_name': 'Test Account'
                }, follow = True)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('withraw'))
        self.assertContains(response, 'Account Does Not exist. Try again')



    def test_successful_withdrawal(self):

        self.client.login(username='testuser', password='testpassword')

        response = {
                'withdraw': '1500',
                'account_no': '123456789',# non-existent account number
                'account_name': 'Test Account'
                }

        self.assertEqual(response.status_code, 302)  # Check if redirected
        self.assertEqual(response.url, reverse('withraw'))
        self.assertContains(response, 'You have withdrawn 500')

        updated_account = Account.objects.get(account_number='123456789')
        self.assertEqual(updated_account.account_balance, 500)






