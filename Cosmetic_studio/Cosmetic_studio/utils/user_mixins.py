from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy

from Cosmetic_studio.accounts.models import Profile


# TODO create mixins for:
# RestrictedUserAccessMixin - only for superusers or owners extends LoginRequiredMixin
# LogoutRequiredMixin only for unauthenticated users
# PageRestrictionMixin - only for is_staff and is_superuser extends LoginRequiredMixin
# RestrictedStaffUsers - only for superusers extends LoginRequiredMixin

class RedirectUserMixin:
    redirect_authenticated_users = False  # Set to True to redirect authenticated users to the index page
    redirect_unauthenticated_users = False  # Set to True to redirect unauthenticated users to the login page
    redirect_message = ""

    def dispatch(self, request, *args, **kwargs):
        if self.redirect_authenticated_users and request.user.is_authenticated:
            messages.info(request, self.redirect_message)
            return redirect(self.get_redirect_url())
        if self.redirect_unauthenticated_users and request.user.is_anonymous:
            messages.info(request, self.redirect_message)
            return redirect(self.get_redirect_url())
        return super().dispatch(request, *args, **kwargs)

    def get_redirect_url(self):
        if self.redirect_unauthenticated_users:
            return reverse_lazy('login_user')
        # Override this to implement logic for redirecting users based on their roles
        return reverse_lazy('index')


class GetProfileMixin:
    def get_object(self, queryset=None):
        pk = self.request.user.pk
        return Profile.objects.get(user_id=pk)
