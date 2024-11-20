from django.contrib.auth import views as auth_views, get_user_model, login
from django.urls import reverse_lazy
from django.views import generic as views
from Cosmetic_studio.accounts.forms import CreateUserForm, StudioUserLoginForm, UpdateProfileForm, ChangePassword
from Cosmetic_studio.accounts.models import Profile
from Cosmetic_studio.utils.user_mixins import RedirectUserMixin, GetProfileMixin
from django.contrib.messages import views as message_views

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
    success_url = reverse_lazy("profile_details")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


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


class ProfileDetailsView(RedirectUserMixin, GetProfileMixin, views.DetailView):
    redirect_unauthenticated_users = True
    redirect_message = "Please Login first to continue"
    model = UserModel
    template_name = "accounts/profile_details.html"


class ProfileUpdateView(RedirectUserMixin, GetProfileMixin, message_views.SuccessMessageMixin,
                        views.UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = "accounts/edit_profile.html"
    success_url = reverse_lazy("profile_details")
    redirect_unauthenticated_users = True
    redirect_message = "Please Login first to continue"
    success_message = "Profile updated successfully."


class UserDeleteView(RedirectUserMixin, message_views.SuccessMessageMixin, views.DeleteView):
    model = UserModel
    template_name = "accounts/delete_profile.html"
    success_url = reverse_lazy("index")
    redirect_unauthenticated_users = True
    redirect_message = "Please Login first to continue"
    success_message = "Profile deleted successfully."

    def get_object(self, queryset=None):
        return self.request.user


class UserChangePasswordView(RedirectUserMixin, message_views.SuccessMessageMixin, auth_views.PasswordChangeView):
    form_class = ChangePassword
    template_name = "accounts/change_password.html"
    success_url = reverse_lazy("profile_details")
    success_message = "Password changed successfully."
    redirect_unauthenticated_users = True
    redirect_message = "Please Login first to continue"
