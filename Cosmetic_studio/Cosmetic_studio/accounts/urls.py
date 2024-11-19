from django.urls import path

from Cosmetic_studio.accounts.views import RegisterUserView, LoginUserView, LogoutPageView, LogoutUserView, \
    ProfileDetailsView

urlpatterns = (
    path('register/', RegisterUserView.as_view(), name='register_user'),
    path('login/', LoginUserView.as_view(), name='login_user'),
    path('logout-page/', LogoutPageView.as_view(), name='logout-page'),
    path('logout/', LogoutUserView.as_view(), name='logout_user'),
    path('details/', ProfileDetailsView.as_view(), name='profile_details'),

)
