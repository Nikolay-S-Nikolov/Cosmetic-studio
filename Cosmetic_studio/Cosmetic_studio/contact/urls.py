from django.urls import path

from Cosmetic_studio.contact.views import ContactPageInfo

urlpatterns = (
    path('', ContactPageInfo.as_view(), name='contact'),
    path('success/', ContactPageInfo.as_view(), name='contact_success'),
)
