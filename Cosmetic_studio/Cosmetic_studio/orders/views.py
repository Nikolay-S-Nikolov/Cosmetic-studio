from django.contrib import messages
from django.contrib.auth import mixins as auth_mixins
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import generic as views

from Cosmetic_studio.orders.forms import CheckoutForm
from Cosmetic_studio.orders.models import Cart, CartItem, OrderItem
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
    template_name = "orders/cart_summary.html"
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


class CheckoutView(auth_mixins.LoginRequiredMixin, views.FormView):
    template_name = 'orders/checkout.html'
    form_class = CheckoutForm
    # success_url = reverse_lazy('order_confirmation') # TODO: Update this to redirect to the order confirmation page
    success_url = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        if not self.get_cart_items().exists():
            print('Checked')
            messages.warning(request, "Your cart is empty. Please add items before proceeding to checkout.")
            return redirect('cart_summary')
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_items = self.get_cart_items()
        context['cart_items'] = cart_items
        context['total'] = self.calculate_total_price(cart_items)
        return context

    def form_valid(self, form):
        cart_items = self.get_cart_items()

        if not cart_items.exists():  # extra safety check
            messages.error(self.request, "Your cart is empty. Unable to process the order.")
            return redirect('cart_summary')



        order = form.save()

        OrderItem.objects.bulk_create([
            OrderItem(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            ) for cart_item in cart_items
        ])

        cart_items.delete()

        messages.success(self.request, "Your order has been placed successfully!")
        return super().form_valid(form)

    @staticmethod
    def calculate_total_price(items):
        total_price = sum(item.product.price * item.quantity for item in items)
        return total_price

    def get_cart_items(self):
        return CartItem.objects.filter(cart__user=self.request.user).select_related('product').all()
