from django.urls import path, include

from Cosmetic_studio.services.views import CreateServiceView, CreateServicePricingView, CreateServicePicturesView, \
    ServicesView, ServiceDetailsView

urlpatterns = (
    path("", include([
        path("", ServicesView.as_view(), name="services"),
        path("create/", CreateServiceView.as_view(), name="create_service"),
        path("<int:pk>/", include([
            path("details/", ServiceDetailsView.as_view(), name="details_service"),
            # path("pricing/", include([
            #     path("<int:pk>/", include([
            #         path("details/", ServiceDetailsView.as_view(), name="details_service_picture"),
            ]))
    ])),
    path("cretae_pricing/", CreateServicePricingView.as_view(), name="create_service_pricing"),
    path("cretae_picture/", CreateServicePicturesView.as_view(), name="create_service_picture"),
)
