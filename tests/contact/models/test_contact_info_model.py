from django.core.exceptions import ValidationError
from django.test import TestCase
from Cosmetic_studio.contact.models import ContactInfo


class ContactInfoModelTest(TestCase):

    def test__create_contact_info__with_valid_phone_number(self):
        contact_info = ContactInfo.objects.create(
            phone_number='0888123456',
            working_time='Mon-Fri 9am-5pm',
            address='123 Main str, Sofia',
            custom_message='Welcome to our contact page!',
        )
        self.assertIsNotNone(contact_info)
        self.assertEqual(contact_info.phone_number, '0888123456')
        self.assertEqual(contact_info.working_time, 'Mon-Fri 9am-5pm')
        self.assertEqual(contact_info.address, '123 Main str, Sofia')
        self.assertEqual(contact_info.custom_message, 'Welcome to our contact page!')
        self.assertTrue(contact_info.visible)
        self.assertIsNotNone(contact_info.created_at)

    def test__phone_number__longer_than_max_length__raises_validation_error(self):
        contact_info = ContactInfo(
            phone_number='08881234567',  # 11 digits, should be invalid
            working_time='Mon-Fri 9am-5pm',
            address='123 Main St, Sofia',
            custom_message='Welcome to our contact page!',
        )
        with self.assertRaises(ValidationError):
            contact_info.full_clean()

    def test__phone_number__shorter_than_10_digits__raises_validation_error(self):
        contact_info = ContactInfo(
            phone_number='08881234',
            working_time='9 AM - 5 PM',
            address='123 Main St',
            custom_message='Welcome to our office.'
        )
        with self.assertRaises(ValidationError):
            contact_info.full_clean()

    def test__phone_number_with_non_numeric_characters__raises_validation_error(self):
        contact_info = ContactInfo(
            phone_number='0888abcd56',
            working_time='9 AM - 5 PM',
            address='123 Main St',
            custom_message='Welcome to our contact page!',
        )
        with self.assertRaises(ValidationError):
            contact_info.full_clean()

    def test__contact_info__str_method__returns_correct_string_representation(self):
        contact_info = ContactInfo.objects.create(
            phone_number="0888123456",
            working_time="Mon-Fri 9am-5pm",
            address="123 Main St, Sofia",
            custom_message="Welcome to our contact page!",
            visible=True
        )
        self.assertEqual(str(contact_info), "Contact Information: 0888123456")