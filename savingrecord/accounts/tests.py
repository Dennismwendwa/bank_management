from django.test import TestCase, Client
from django.contrib.auth.models import User

# Create your tests here.
class AccountViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
    
    def test_register_view_invalid_password(self):
        response = self.client.post('/register/', {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'email': 'johndoe@example.com',
            'password1': '1234567',  # Less than 8 characters
            'password2': '1234567',
        }, follow=True)  # Add the follow=True parameter)
#       print(response.status_code)
#       print(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, '/accounts/register/')

        # Assert that the error message is displayed
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'The Password Must be 8 or more charactors!')
