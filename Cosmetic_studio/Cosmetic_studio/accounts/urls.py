from django.urls import path

from Cosmetic_studio.accounts.views import RegisterUserView
from Cosmetic_studio.common.views import index, login, signup, signout, profile_details, edit_profile, delete_profile

urlpatterns = (
    path('register/', RegisterUserView.as_view(), name='register_user'),
)
