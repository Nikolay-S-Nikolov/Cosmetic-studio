
from django.test import TestCase
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.test import RequestFactory

from Cosmetic_studio.blog.models import Tag, BlogContent
from Cosmetic_studio.contact.views import ContactPageInfo

UserModel = get_user_model()


class ContactPageInfoTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user_data = {
            'email': 'testuser@gmail.com',
            'password': '123qwer'
        }
        self.user = UserModel.objects.create_user(**self.user_data)
        self.view = ContactPageInfo()
        self.view.request = self.factory.get(reverse_lazy('contact'))
        self.view.request.user = self.user

    def test__get_initial__authenticated_user__when_no_name_provided(self):
        self.client.login(**self.user_data)
        request = self.factory.get(reverse_lazy('contact'))
        request.user = self.user
        self.view.request = request

        initial_data = self.view.get_initial()

        self.assertEqual(initial_data['name'], '')
        self.assertEqual(initial_data['email'], self.user.email)

    def test__get_initial__authenticated_user__with_name_provided(self):
        self.user.profile.preferred_name_nickname = 'Arnold Schwarzenegger'
        self.client.login(**self.user_data)
        request = self.factory.get(reverse_lazy('contact'))
        request.user = self.user
        self.view.request = request

        initial_data = self.view.get_initial()

        self.assertEqual(initial_data['name'], self.user.profile.get_profile_name())
        self.assertEqual(initial_data['email'], self.user.email)

    def test__contact_page_info__redirects_on_successful_form_submission(self):
        self.client.login(**self.user_data)

        response = self.client.post(reverse_lazy('contact'), {
            'name': 'Gosho',
            'email': 'gosho@abv.com',
            'phone': '0888123456',
            'message': 'This is a test message.'
        })

        self.assertRedirects(response, reverse_lazy('contact_success'))

    def test__contact_page_info__form_submission_errors(self):
        response = self.client.post(reverse_lazy('contact'), data={})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact/contact_info.html')
        self.assertContains(response, 'This field is required')
        self.assertIn('form', response.context)
        self.assertTrue(response.context['form'].errors)
