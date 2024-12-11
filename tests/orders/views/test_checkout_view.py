from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from Cosmetic_studio.orders.models import Cart, CartItem, Order
from Cosmetic_studio.orders.views import CheckoutView
from Cosmetic_studio.product.models import Product

UserModel = get_user_model()


class CheckoutViewTest(TestCase):
    def setUp(self):
        self.user_data = {
            'email': 'lili@gmail.com',
            'password': '1123qWER',
        }
        self.user = UserModel.objects.create_user(**self.user_data)
        self.client.login(**self.user_data)

        self.product_data = {
            'name': 'New Product',
            'price': 10,
            'slug': 'new-product'
        }
        self.product = Product.objects.create(**self.product_data)

        self.cart = Cart.objects.create(user=self.user)
        self.cart_item = CartItem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=1
        )

        self.url = reverse('checkout_order')

        self.order_data = {
            'name': 'Arnold Schwarzenegger',
            'phone_number': '0987654321',
            'email': 'Arnold@gmail.com',
            'address': '2 Dondukov Blvd.',
            'city': 'Sofia',
            'postal_code': '1000',
            'payment_method': 'pay_on_delivery',
        }

    def test__dispatch__when_cart_is_empty__redirects_to_cart_summary(self):
        self.cart_item.delete()

        response = self.client.get(self.url)

        self.assertRedirects(response, reverse('cart_summary'))

        messages = list(response.wsgi_request._messages)

        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Your cart is empty. Please add items before proceeding to checkout.")

    def test__calculate_total_price__for_cart_items(self):
        cart_items = CartItem.objects.filter(cart=self.cart)
        total_price = CheckoutView.calculate_total_price(cart_items)

        self.assertEqual(total_price, 10)

        product1 = Product.objects.create(
            name='Product 1',
            price=15,
            slug='product-1'
        )
        product2 = Product.objects.create(
            name='Product 2',
            price=20,
            slug='product-2'
        )

        CartItem.objects.create(cart=self.cart, product=product1, quantity=2)
        CartItem.objects.create(cart=self.cart, product=product2, quantity=3)

        cart_items = CartItem.objects.filter(cart=self.cart)
        total_price = CheckoutView.calculate_total_price(cart_items)

        self.assertEqual(total_price, 10 + 2 * 15 + 3 * 20)

    def test__checkout_view__increases_product_units_sold__redirects_to_confirmation(self):
        self.cart_item.quantity = 3
        self.cart_item.save()

        response = self.client.post(
            self.url,
            data=self.order_data,
        )

        self.product.refresh_from_db()
        self.assertEqual(self.product.units_sold, 3)

        self.assertRedirects(
            response,
            reverse(
                'order_confirmation',
                kwargs={'pk': Order.objects.first().id}
            ),
        )

    def test__checkout_view__deletes_cart_items__after_checkout(self):
        self.client.post(
            self.url,
            data=self.order_data,
        )

        self.assertFalse(CartItem.objects.filter(cart=self.cart).exists())

    def test__checkout_view__success_message__after_checkout(self):
        response = self.client.post(
            self.url,
            data=self.order_data,
            follow=True
        )

        self.assertContains(response, "Your order has been placed successfully!")

    def test__checkout_view__loads_cart_items_and_total_price_in_context(self):

        product1 = Product.objects.create(name='Product 1', price=10.00, slug='product-1')
        product2 = Product.objects.create(name='Product 2', price=20.00, slug='product-2')

        CartItem.objects.create(cart=self.cart, product=product1, quantity=2)
        CartItem.objects.create(cart=self.cart, product=product2, quantity=1)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/checkout.html')
        self.assertIn('cart_items', response.context)
        self.assertIn('total', response.context)

        cart_items = response.context['cart_items']
        total = response.context['total']

        self.assertEqual(cart_items.count(), 3)
        self.assertEqual(total, 50.00)
