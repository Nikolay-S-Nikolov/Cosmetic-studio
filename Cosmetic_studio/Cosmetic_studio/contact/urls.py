from django.urls import path

from Cosmetic_studio.contact.views import ContactPageInfo

urlpatterns = (
    path('', ContactPageInfo.as_view(), name='contact'),
)
