from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from Cosmetic_studio.accounts.forms import CreateUserForm


UserModel = get_user_model()


class TestRegisterUserView(TestCase):
    def setUp(self):
        self.register_url = reverse('register_user')
        self.profile_details_url = reverse('profile_details')
        self.user = UserModel.objects.create_user(
            user_name='Noname',
            email='name@gmail.com',
            password='1123qWER')
        self.user_data = {
            'email': 'newuser@gmail.com',
            'user_name': 'My Name',
            'password1': '1123qWER',
            'password2': '1123qWER',

        }

    def test__register_view__redirects_authenticated_users__to_index(self):
        self.client.login(email='name@gmail.com', password='1123qWER')
        response = self.client.get(self.register_url)
        self.assertRedirects(response, reverse('index'))
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "You are already logged in. Please log out first.")

    def test__register_user__when_valid_data(self):
        user_data = {
            'email': 'newuser@gmail.com',
            'user_name': 'My Name',
            'password1': '1123qWER',
            'password2': '1123qWER',
        }

        response = self.client.post(self.register_url, user_data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.profile_details_url)
        self.assertTrue(UserModel.objects.filter(email='newuser@gmail.com').exists())
        user = UserModel.objects.get(email='newuser@gmail.com')
        self.assertTrue(user.is_authenticated)

    def test__register_user_view__with_invalid_email(self):
        invalid_data = {
            'email': 'nodot@email',
            'password1': '123aWER',
            'password2': '123qWER',
        }
        response = self.client.post(self.register_url, data=invalid_data)
        self.assertEqual(response.status_code, 200)

        form = response.context['form']
        self.assertTrue(form.errors)
        self.assertIn('Enter a valid email address.', form.errors['email'])
        self.assertIn('The two password fields didn’t match.', form.errors['password2'])

