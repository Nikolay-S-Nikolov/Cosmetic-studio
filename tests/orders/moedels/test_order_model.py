from django.test import TestCase
from django.contrib.auth import get_user_model

from Cosmetic_studio.orders.models import Order

UserModel = get_user_model()


class OrderModelTest(TestCase):
    def setUp(self):
        self.user_data = {
            'email': 'arnold@studio.com',
            'password': '1123qWER'
        }
        self.user = UserModel.objects.create(**self.user_data)

    def test__create_order__with_default_status_pending(self):
        order = Order.objects.create(
            customer=self.user,
            total_price=100.00
        )
        self.assertEqual(order.status, 'Pending')

    def test__order_association_with_customer_and_deletion_on_customer_delete(self):
        order = Order.objects.create(customer=self.user, total_price=100.00)

        self.assertEqual(order.customer, self.user)

        self.user.delete()

        with self.assertRaises(order.DoesNotExist):
            Order.objects.get(id=order.id)

    def test__str__returns_correct_format(self):
        order = Order.objects.create(customer=self.user, status='Processing', total_price=100.00)
        expected = f"Order #{order.id} - Processing"
        self.assertEqual(str(order), expected)
