from django.contrib.auth import views as auth_views, get_user_model
from django.contrib.auth import mixins as auth_mixins
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic as views

from Cosmetic_studio.accounts.forms import CreateUserForm, StudioUserLoginForm
from Cosmetic_studio.accounts.models import Profile
from Cosmetic_studio.utils.user_mixins import RedirectUserMixin

UserModel = get_user_model()


# TODO cerate mixins for:
# RestrictedUserAccessMixin - only for superusers or owners extends LoginRequiredMixin
# LogoutRequiredMixin only for unauthenticated users
# PageRestrictionMixin - only for is_staff and is_superuser extends LoginRequiredMixin
# RestrictedStaffUsers - only for superusers extends LoginRequiredMixin

class RegisterUserView(RedirectUserMixin, views.CreateView):
    redirect_authenticated_users = True
    redirect_message = "You are already logged in. Please log out first."
    template_name = "accounts/register.html"
    form_class = CreateUserForm
    success_url = reverse_lazy("index")  # TODO to redirect to profile details page after successful registration


class LoginUserView(RedirectUserMixin, auth_views.LoginView):
    redirect_authenticated_users = True
    redirect_message = "You are already logged in."
    form_class = StudioUserLoginForm
    template_name = "accounts/login.html"


class LogoutPageView(RedirectUserMixin, views.TemplateView):
    redirect_unauthenticated_users = True
    redirect_message = "Please Login first to continue"
    template_name = "accounts/signout.html"


class LogoutUserView(auth_views.LogoutView):
    pass


class ProfileDetailsView(RedirectUserMixin, views.DetailView):
    redirect_unauthenticated_users = True
    redirect_message = "Please Login first to continue"
    model = UserModel
    template_name = "accounts/profile_details.html"

    def get_object(self, queryset=None):
        return self.request.user.profile



