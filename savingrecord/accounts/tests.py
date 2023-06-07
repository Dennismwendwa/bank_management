from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.shortcuts import reverse
from accounts.models import Profile
from accounts.forms import UserUpdateForm, ProfileUpdateForm

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


	#test 2
    def test_register_view_success(self):
        response = self.client.post(reverse('register'), {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'email': 'johndoe@example.com',
            'password1': 'password123',
            'password2': 'password123',
        }, follow=True)

#       self.assertRedirects(response, '/saving/')
#       self.assertEqual(response.status_code, 200)

#       print(response.content)
#print(response.status_code)
        # Assert that the user was created
        self.client.login(username='johndoe', password='password123')
	# Access the /savings/ URL
#        response = self.client.post(reverse('register'), data=self.valid_data)
#        self.assertRedirects(response, reverse('saving'))
#        response = self.client.get('/saving/')
#self.assertEqual(response.status_code, 200) 
        self.assertTrue(User.objects.filter(username='johndoe').exists())
