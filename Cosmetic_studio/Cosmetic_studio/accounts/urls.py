from django.urls import path

from Cosmetic_studio.accounts.views import RegisterUserView, LoginUserView, LogoutPageView, LogoutUserView, \
    ProfileDetailsView, ProfileUpdateView, UserDeleteView

urlpatterns = (
    path('register/', RegisterUserView.as_view(), name='register_user'),
    path('login/', LoginUserView.as_view(), name='login_user'),
    path('logout-page/', LogoutPageView.as_view(), name='logout-page'),
    path('logout/', LogoutUserView.as_view(), name='logout_user'),
    path('details/', ProfileDetailsView.as_view(), name='profile_details'),
    path('edit-profile/', ProfileUpdateView.as_view(), name='edit_profile'),
    path('delete-profile/', UserDeleteView.as_view(), name='delete_profile'),

)
