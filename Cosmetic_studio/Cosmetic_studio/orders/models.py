from django.contrib.auth import get_user_model
from django.db import models

from Cosmetic_studio.product.models import Product

UserModel = get_user_model()


class Order(models.Model):

    MAX_STATUS_LENGTH = 10
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    customer = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

    status = models.CharField(
        max_length=MAX_STATUS_LENGTH,
        choices=STATUS_CHOICES,
        default='Pending',
    )

    total_price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return f"Order #{self.id} - {self.status}"


class OrderItem(models.Model):
    """
    Links products to orders.
    """

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField()

    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
    )

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"


class Cart(models.Model):
    user = models.OneToOneField(
        UserModel,
        on_delete=models.CASCADE,
        null=True, blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(
        default=1,
    )

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"


class ShippingAddress(models.Model):
    MAX_CITY_LENGTH = 50

    customer = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE
    )

    address = models.TextField()

    city = models.CharField(
        max_length=MAX_CITY_LENGTH,
    )

    postal_code = models.CharField(
        max_length=10,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return f"Shipping for Order #{self.order.id}"