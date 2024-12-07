from django.urls import path, include

from Cosmetic_studio.services.views import CreateServiceView, CreateServicePricingView, CreateServicePicturesView, \
    ServicesView, ServiceDetailsView, UpdateServiceView, DeleteServiceView, UpdatePricingView, DeletePricingView, \
    DeleteServicePicturesView

urlpatterns = (
    path("", include([
        path("", ServicesView.as_view(), name="services"),
        path("create/", CreateServiceView.as_view(), name="create_service"),
        path("<int:pk>/", include([
            path("details/", ServiceDetailsView.as_view(), name="details_service"),
            path("update/", UpdateServiceView.as_view(), name="update_service"),
            path("delete/", DeleteServiceView.as_view(), name="delete_service"),
            path("update-pricing/", UpdatePricingView.as_view(), name="update_pricing"),
            path("delete-pricing/", DeletePricingView.as_view(), name="delete_pricing"),
            path("delete-picture/", DeleteServicePicturesView.as_view(), name="delete_picture"),
            ]))
    ])),
    path("cretae_pricing/", CreateServicePricingView.as_view(), name="create_service_pricing"),
    path("cretae_picture/", CreateServicePicturesView.as_view(), name="create_service_picture"),
)
