from django.contrib import messages
from django.contrib.auth import mixins as auth_mixins
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
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


class UpdateCartItemView(auth_mixins.LoginRequiredMixin, views.View):

    def post(self, request, pk):
        cart_item = get_object_or_404(CartItem, pk=pk, cart__user=request.user)

        if self.request.user != cart_item.cart.user:  # redundant check as an  extra layer of security
            raise PermissionDenied("You don't have permission to modify this cart item.")

        action = request.POST.get('action')

        if action == 'increase':
            cart_item.quantity += 1
        else:
            cart_item.quantity = max(1, cart_item.quantity - 1)

        cart_item.save()
        messages.success(request, f"{cart_item.product.name} quantity updated to {cart_item.quantity}.")
        return HttpResponseRedirect(reverse('cart_summary'))


class RemoveFromCartView(auth_mixins.LoginRequiredMixin, views.View):
    def post(self, request, pk):
        cart_item = get_object_or_404(CartItem, pk=pk, cart__user=request.user)

        if self.request.user != cart_item.cart.user:  # redundant check as an  extra layer of security
            raise PermissionDenied("You don't have permission to remove this cart item.")

        product_name = cart_item.product.name
        cart_item.delete()
        messages.success(request, f"{product_name} removed from your cart.")
        return HttpResponseRedirect(reverse('cart_summary'))
