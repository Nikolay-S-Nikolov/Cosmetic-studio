from django.urls import path

from Cosmetic_studio.common.views import index

urlpatterns = (
    path('', index, name='index'),
)
