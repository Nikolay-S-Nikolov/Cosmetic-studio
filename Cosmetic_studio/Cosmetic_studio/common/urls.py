from django.urls import path

from Cosmetic_studio.common.views import index, signout,profile_details,edit_profile,delete_profile

urlpatterns = (
    path('', index, name='index'),
    path('signout/', signout, name='signout'),
    path('account-details/', profile_details, name='profile_details'),
    path('edit-profile/', edit_profile, name='edit_profile'),
    path('delete-profile/', delete_profile, name='delete_profile'),
)
