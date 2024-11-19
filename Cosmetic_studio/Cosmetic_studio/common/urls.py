from django.urls import path

from Cosmetic_studio.common.views import index, edit_profile,delete_profile

urlpatterns = (
    path('', index, name='index'),
    path('edit-profile/', edit_profile, name='edit_profile'),
    path('delete-profile/', delete_profile, name='delete_profile'),
)
