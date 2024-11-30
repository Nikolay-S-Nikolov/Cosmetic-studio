from django.urls import include, path

from Cosmetic_studio.product.views import DetailsProductView, ListProductsView

urlpatterns = (
    path('product/', include([
        path('', ListProductsView.as_view(), name='list_products'),
        path('details/<slug:slug>/', DetailsProductView.as_view(), name='details_product'),
    ])),
)
