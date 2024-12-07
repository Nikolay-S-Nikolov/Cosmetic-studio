from django.urls import path

from Cosmetic_studio.contact.views import ContactPageInfo,ContactSuccessPageInfo, AsyncEmailView

urlpatterns = (
    path('', ContactPageInfo.as_view(), name='contact'),
    path('async_send_email/', AsyncEmailView.as_view(), name='async_send_email'),
    path('success/', ContactSuccessPageInfo.as_view(), name='contact_success'),
)
