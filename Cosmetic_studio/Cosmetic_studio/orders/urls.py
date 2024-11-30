from django.urls import path, include

from Cosmetic_studio.orders.views import AddToCartView, CartSummaryView

urlpatterns = (
    path('<slug:slug>/', include([
        path('add-to-cart/', AddToCartView.as_view(), name='add_to_cart'),
    ])),
    path('cart/', CartSummaryView.as_view(), name='cart_summary'),
)
