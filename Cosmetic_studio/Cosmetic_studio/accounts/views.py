from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic as views

from Cosmetic_studio.accounts.forms import CreateUserForm


# TODO cerate mixins for:
# RestrictedUserAccessMixin - only for superusers or owners extends LoginRequiredMixin
# LogoutRequiredMixin only for unauthenticated users
# PageRestrictionMixin - only for is_staff and is_superuser extends LoginRequiredMixin
# RestrictedStaffUsers - only for superusers extends LoginRequiredMixin

class RegisterUserView(views.CreateView):
    template_name = "accounts/register.html"
    form_class = CreateUserForm
    success_url = reverse_lazy("index")  # TODO to redirect to profile update page after successful registration


def create_user(request):
    pass
