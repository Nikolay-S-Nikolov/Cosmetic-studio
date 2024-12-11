from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from Cosmetic_studio.accounts.models import Profile

UserModel = get_user_model()


class ProfileModelTest(TestCase):
    def test__create_profile__with_default_values(self):
        user = UserModel.objects.create(email='myName@gmail.com', password='123qWER')
        profile = Profile.objects.get(user=user)

        self.assertEqual(profile.preferred_name_nickname, "Anonymous")
        self.assertIsNone(profile.phone_number)
        self.assertIsNone(profile.profile_picture)
        self.assertEqual(profile.get_profile_name(), "Anonymous")

    def test__get_profile_name__returns_preferred_name(self):
        user = UserModel.objects.create(email='myName@gmail.com', password='123qWER', user_name="My Name")
        profile = Profile.objects.get(user=user)

        self.assertEqual(profile.get_profile_name(), 'Anonymous')

        profile.preferred_name_nickname = "Nickname Name"
        self.assertEqual(profile.get_profile_name(), 'Nickname Name')

    def test__phone_number__validation(self):
        user = UserModel.objects.create(email='myName@gmail.com', password='123qWER', user_name="My Name")
        profile = Profile.objects.get(user=user)

        profile.phone_number = '0888123456'
        profile.full_clean()

        invalid_numbers = ['1234567890', '088812345', '08881234567', 'abcdefghij']
        for number in invalid_numbers:
            profile.phone_number = number
            with self.assertRaises(ValidationError) as ve:
                profile.full_clean()

