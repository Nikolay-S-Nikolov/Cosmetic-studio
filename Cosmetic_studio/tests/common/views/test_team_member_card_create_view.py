from io import BytesIO

from PIL import Image
from django.contrib.messages import get_messages
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse_lazy, reverse
from django.contrib.auth import get_user_model
from django.test import RequestFactory
from Cosmetic_studio.common.views import TeamMemberCardCreateView
from Cosmetic_studio.common.models import TeamMemberCard

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


class TestTeamMemberCardCreateView(TestCase):

    def setUp(self):
        self.user_data = {'email': 'myname@gmail.com', 'password': '123qWER'}
        self.factory = RequestFactory()
        self.user = UserModel.objects.create_user(**self.user_data)
        picture = generate_test_image()
        featured_image = generate_test_image()
        about_image = generate_test_image()

        self.card_data = {
            'name': 'Arnold Schwarzenegger',
            'picture': picture,
            'featured_image': featured_image,
            'about_image': about_image,
            'title': 'Test Title',
            'description': 'Some description here',
            'role': 'No role provided',
            'specialities': 'Specialities here',
            'is_active': True,
            'appearance_order': 2,
        }

    def test__create_team_member_card__with_valid_data__user_not_staff__returns_403(self):
        self.assertFalse(self.user.is_staff)
        self.client.login(**self.user_data)

        response = self.client.post(reverse_lazy('create_team_member'), self.card_data)
        self.assertEqual(response.status_code, 403)
        self.assertFalse(TeamMemberCard.objects.filter(name='Arnold Schwarzenegger').exists())

    def test__create_team_member_card__with_valid_data__user_is_staff__returns_302(self):
        self.user.is_staff = True
        self.user.save()

        self.client.login(**self.user_data)
        response = self.client.post(reverse_lazy('create_team_member'), self.card_data, format='multipart')

        self.assertEqual(response.status_code, 302)
        if response.context and 'form' in response.context:
            if response.context and 'form' in response.context:
                print("Form errors:", response.context['form'].errors)
                print("Form cleaned data:", response.context['form'].cleaned_data)

        self.assertTrue(TeamMemberCard.objects.filter(name='Arnold Schwarzenegger').exists())
        self.assertTrue(self.user.is_staff)

    def test__create_team_member_card__with_valid_data__user_is_staff__check_created_by_correct(self):
        self.user.is_staff = True
        self.user.save()

        self.client.login(**self.user_data)
        self.client.post(reverse_lazy('create_team_member'), self.card_data)

        self.assertTrue(TeamMemberCard.objects.get(name='Arnold Schwarzenegger').created_by == self.user)

    def test__team_member_card_create_view__redirects_to_success_url(self):
        self.user.is_staff = True
        self.user.save()

        self.client.force_login(self.user)
        response = self.client.post(reverse('create_team_member'), self.card_data)
        self.assertRedirects(response, reverse('index'))

    def test__team_member_card_create_view__returns_correct_success_message(self):
        self.user.is_staff = True
        self.user.save()
        self.client.force_login(self.user)

        response = self.client.post(reverse('create_team_member'), self.card_data)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Team member 'Arnold Schwarzenegger' was successfully created.")

