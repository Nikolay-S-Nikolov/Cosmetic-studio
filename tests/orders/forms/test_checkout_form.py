from django.test import TestCase
from django.contrib.auth import get_user_model
from Cosmetic_studio.orders.forms import CheckoutForm
from Cosmetic_studio.orders.models import ShippingAddress, Order, Cart
from Cosmetic_studio.product.models import Product

UserModel = get_user_model()


class CheckoutFormTest(TestCase):
    def setUp(self):
        self.user_data = {
            'email': 'lili@gmail.com',
            'password': '1123qWER',
        }
        self.user = UserModel.objects.create_user(**self.user_data)
        self.address_data = {
            'name': 'Arnold Schwarzenegger',
            'phone_number': '0987654321',
            'email': 'Arnold@gmail.com',
            'address': '2 Dondukov Blvd.',
            'city': 'Sofia',
            'postal_code': '1000',
            'payment_method': 'pay_on_delivery',
        }
        self.order = Order.objects.create(
            customer=self.user,
            total_price=100,
        )

        self.shipping_address = ShippingAddress.objects.create(**self.address_data, customer=self.user,
                                                               order=self.order)

    def test__checkout_form__initializes_with_last_order_data(self):
        previous_order = self.order

        form = CheckoutForm(user=self.user)

        self.assertEqual(form.fields['name'].initial, previous_order.shippingaddress.name)
        self.assertEqual(form.fields['phone_number'].initial, previous_order.shippingaddress.phone_number)
        self.assertEqual(form.fields['email'].initial, previous_order.shippingaddress.email)
        self.assertEqual(form.fields['address'].initial, previous_order.shippingaddress.address)
        self.assertEqual(form.fields['city'].initial, previous_order.shippingaddress.city)
        self.assertEqual(form.fields['postal_code'].initial, previous_order.shippingaddress.postal_code)

    def test__initialize_form_fields__with_user_data__no_previous_orders(self):
        new_user = UserModel.objects.create_user(
            email='someone@gmail.com',
            password='123qwer',
        )

        new_user.profile.phone_number = '0888123456'
        new_user.profile.save()

        form = CheckoutForm(user=new_user)

        self.assertEqual(form.fields['name'].initial, new_user.user_name)
        self.assertEqual(form.fields['phone_number'].initial, new_user.profile.phone_number)
        self.assertEqual(form.fields['email'].initial, new_user.email)
        self.assertEqual(form.fields['address'].initial, None)
        self.assertEqual(form.fields['city'].initial, None)
        self.assertEqual(form.fields['postal_code'].initial, None)

    def test__save_order_commit_true__create_shipping_address(self):
        cart = Cart.objects.create(user=self.user)
        product = Product.objects.create(name='Test Product', price=10)
        cart.items.create(product=product, quantity=2)

        new_address_data = {
            'name': 'Rumen Radev',
            'phone_number': '0888111222',
            'email': 'press@president.bg',
            'address': '16 Vitoshko Lale Str',
            'city': 'Sofia',
            'postal_code': '1616',
            'payment_method': 'pay_on_delivery',

        }

        form = CheckoutForm(data=new_address_data, user=self.user)
        self.assertTrue(form.is_valid())

        order = form.save(commit=True)

        self.assertIsNotNone(order.id)
        self.assertEqual(order.customer, self.user)
        self.assertEqual(order.total_price, 20)
        self.assertEqual(order.status, 'Pending')

        shipping_address = ShippingAddress.objects.get(order=order)
        self.assertEqual(shipping_address.name, new_address_data.get('name'))
        self.assertEqual(shipping_address.phone_number, new_address_data.get('phone_number'))
        self.assertEqual(shipping_address.email, new_address_data.get('email'))
        self.assertEqual(shipping_address.address, new_address_data.get('address'))
        self.assertEqual(shipping_address.city, new_address_data.get('city'))
        self.assertEqual(shipping_address.postal_code, new_address_data.get('postal_code'))
