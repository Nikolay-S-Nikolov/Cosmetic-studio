from django.urls import path

from Cosmetic_studio.contact.views import ContactPageInfo,ContactSuccessPageInfo

urlpatterns = (
    path('', ContactPageInfo.as_view(), name='contact'),
    path('success/', ContactSuccessPageInfo.as_view(), name='contact_success'),
)
