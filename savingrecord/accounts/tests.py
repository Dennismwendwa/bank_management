from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.shortcuts import reverse
from accounts.models import Profile
from django.contrib import messages
from accounts.forms import UserUpdateForm, ProfileUpdateForm

# Create your tests here.
class AccountViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

#   Test1
    def test_register_view_invalid_password(self):
        response = self.client.post(reverse('register'), {
            'first_name': 'millicent',
            'last_name': 'wand',
            'username': 'milly1',
            'email': 'millicent@example.com',
            'password1': '1234567',  # Less than 8 characters
            'password2': '1234567',
        }, follow=True)  # Add the follow=True parameter

#      assert that registration was unsessessful and user not redirected
        self.assertTemplateUsed(response, "accounts/register.html")

#	assert that  form validation error message is didplayed
        messages = [m.message for m in response.context["messages"]]
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0], "The Password Must be 8 or more characters!")

#       check that user was not created in database
        self.assertFalse(User.objects.filter(username="milly1").exists())

#   Test 2
    def test_register_view_success(self):
        response = self.client.post(reverse('register'), {
            'first_name': 'millicent',
            'last_name': 'wand',
            'username': 'millicent',
            'email': 'millicent@example.com',
            'password1': 'password123',
            'password2': 'password123',
        }, follow=True)

#       assert that registration was successful and user redirected
        self.assertRedirects(response, "/accounts/login/?next=/")

#       check if user was created in database
        self.assertTrue(User.objects.filter(username="millicent").exists())

#     Test 3
    def test_register_password_not_matching(self):
        response = self.client.post(reverse("register"), {
            'first_name': 'millicent',
	    'last_name': 'wand',
	    'username': 'millicent',
	    'email': 'millicent@example.com',
	    'password1': 'password123',
	    'password2': 'password555',
        }, follow=True)

#       assert password not matching
        messages = [m.message for m in response.context["messages"]]
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0], "Password not matching")

#       assert that registration was unsuccessful and user not redirected
        self.assertTemplateUsed(response, "accounts/register.html")


#       chack user was not created in the database
        self.assertFalse(User.objects.filter(username="milly1").exists())




class AccountViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="milly", password="frontend")

#   Test 4
    def test_login_view_valid_credentials(self):
        response = self.client.post(reverse("login"), {
            "username": "milly",
            "password": "frontend",
        }, follow=True)

#     assert that login was successfull and user redirected
        self.assertRedirects(response, reverse("savings"))

#     assert that user is authenticated
        self.assertTrue(response.context["user"].is_authenticated)


#   Test 5
    def test_login_view_invalid_credentials(self):
        response = self.client.post(reverse("login"), {
            "username": "milly",
            "password": "wrongpasswd",
        }, follow=True)


#        assert that login was unseccessfull and redicted back to login
        self.assertTemplateUsed(response, "accounts/login.html")

#       assert form validation error message is displayed
        messages = [m.message for m in response.context["messages"]]
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0], "Invalid credentials")

#       assert that user is not authenticated
        self.assertFalse(response.context["user"].is_authenticated)
