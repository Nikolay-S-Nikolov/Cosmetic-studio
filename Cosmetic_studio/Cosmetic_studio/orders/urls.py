from django.urls import path, include

from Cosmetic_studio.orders.views import AddToCartView, CartSummaryView, UpdateCartItemView, RemoveFromCartView

urlpatterns = (
    path('<slug:slug>/', include([
        path('add-to-cart/', AddToCartView.as_view(), name='add_to_cart'),
    ])),
    path('cart/', CartSummaryView.as_view(), name='cart_summary'),
    path('update-cart-item/<int:pk>/', UpdateCartItemView.as_view(), name='update_cart_item'),
    path('remove-cart-item/<int:pk>/', RemoveFromCartView.as_view(), name='remove_cart_item'),

)
