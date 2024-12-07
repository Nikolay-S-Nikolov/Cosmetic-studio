from django.contrib import messages
from django.contrib.auth import mixins as auth_mixins
from django.views import generic as views


class StaffRequiredMixin(auth_mixins.LoginRequiredMixin, auth_mixins.UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


class CommonMessageMixin:
    success_message = ""
    object_name = "Team member"

    def get_success_message(self):
        return f"{self.object_name} '{self.object.name}' was successfully {self.get_action_verb()}."

    def get_action_verb(self):
        if isinstance(self, views.CreateView):
            return "created"
        elif isinstance(self, views.UpdateView):
            return "updated"
        elif isinstance(self, views.DeleteView):
            return "deleted"
        return "processed"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.get_success_message())
        return response

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        response = super().delete(request, *args, **kwargs)
        messages.success(self.request, self.get_success_message())
        return response
