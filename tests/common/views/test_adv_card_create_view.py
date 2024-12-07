from io import BytesIO

from PIL import Image
from django.contrib.messages import get_messages
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, RequestFactory
from django.urls import reverse, reverse_lazy
from django.contrib.auth import get_user_model
from Cosmetic_studio.common.models import IndexPageAds

UserModel = get_user_model()


def generate_test_image():
    """Creates a simple in-memory test image."""
    image = BytesIO()
    img = Image.new('RGB', (100, 100), color='red')
    img.save(image, format='JPEG')
    image.seek(0)
    return SimpleUploadedFile(
        name='test_image.jpg',
        content=image.read(),
        content_type='image/jpeg'
    )


class AdvCardCreateViewTest(TestCase):
    def setUp(self):
        mock_image = generate_test_image()

        self.user_data = {'email': 'myname@gmail.com', 'password': '123qWER'}
        self.factory = RequestFactory()

        self.user = UserModel.objects.create_user(**self.user_data)

        self.card_data = {
            'name': 'Card Name',
            'adv_description': 'Crad Description',
            'adv_image': mock_image,
            'adv_link': 'https://example.com',
        }
        self.url = reverse('index')

    def test__adv_card_create_view__with_valid_data__user_is_staff__returns_302(self):
        self.user.is_staff = True
        self.user.save()

        self.client.login(**self.user_data)
        response = self.client.post(reverse_lazy('create_adv_card'), self.card_data, format='multipart')

        self.assertEqual(response.status_code, 302)

        self.assertTrue(IndexPageAds.objects.filter(name='Card Name').exists())
        self.assertTrue(self.user.is_staff)

    def test__adv_card_create_view__with_valid_data__user_not_staff__returns_403(self):
        self.client.login(**self.user_data)
        response = self.client.post(reverse_lazy('create_adv_card'), self.card_data, format='multipart')

        self.assertEqual(response.status_code, 403)
        self.assertFalse(IndexPageAds.objects.filter(name='Card Name').exists())
        self.assertFalse(self.user.is_staff)

    def test__adv_card_create_view__with_valid_data__user_is_staff__created_by_correct(self):
        self.user.is_staff = True
        self.user.save()

        self.client.login(**self.user_data)
        self.client.post(reverse_lazy('create_adv_card'), self.card_data)

        self.assertTrue(IndexPageAds.objects.get(name='Card Name').created_by == self.user)

    def test__adv_card_create_view__redirects_to_success_url(self):
        self.user.is_staff = True
        self.user.save()

        self.client.force_login(self.user)
        response = self.client.post(reverse('create_adv_card'), self.card_data, follow=True)
        self.assertRedirects(response, reverse('index'))

    def test_adv_card_create_view_returns_correct_success_message(self):
        self.user.is_staff = True
        self.user.save()
        self.client.force_login(self.user)
        response = self.client.post(reverse('create_adv_card'), self.card_data)
        self.assertRedirects(response, reverse('index'))
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Advertisement 'Card Name' was successfully created.")
