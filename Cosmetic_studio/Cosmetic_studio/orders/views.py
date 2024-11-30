from django.contrib import messages
from django.contrib.auth import mixins as auth_mixins
from django.shortcuts import get_object_or_404, redirect
from django.views import generic as views

from Cosmetic_studio.orders.models import Cart, CartItem
from Cosmetic_studio.product.models import Product
from Cosmetic_studio.services.models import Services


class AddToCartView(auth_mixins.LoginRequiredMixin, views.View):
    def post(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not item_created:
            cart_item.quantity += 1
            cart_item.save()
            messages.info(request, f"The {product.name} quantity was updated to {cart_item.quantity}.")
        else:
            messages.info(request, f"The {product.name} was added to your cart.")
            # TODO check message

        return redirect("details_product", slug=slug)


class CartSummaryView(auth_mixins.LoginRequiredMixin, views.ListView):

    model = CartItem
    template_name = "products/cart_summary.html"
    context_object_name = 'object_list'

    def get_queryset(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart.items.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart.objects.get(user=self.request.user)
        context['total'] = sum(item.product.price * item.quantity for item in cart.items.all())
        context['footer_services'] = Services.objects.order_by("?")[:4]
        return context
