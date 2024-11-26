from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic as views

from Cosmetic_studio.common.models import TeamMemberCard, IndexPageAds


class IndexView(views.ListView):
    model = TeamMemberCard
    template_name = 'common/index.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ads'] = IndexPageAds.objects.all().order_by("-created_at")
        return context


class TeamMemberDetailsView(views.DetailView):
    model = TeamMemberCard
    template_name = 'common/team-member-details.html'


class TeamMemberCardCreateView(views.CreateView):
    model = TeamMemberCard
    fields = '__all__'
    template_name = 'shared_templates/form_template.html'
    extra_context = {
        'form_title': 'Add Team Member',
        'submit_button_text': 'Add',
    }
    success_url = reverse_lazy('index')


class TeamMemberCardUpdateView(views.UpdateView):
    model = TeamMemberCard
    fields = '__all__'
    template_name = 'shared_templates/form_template.html'
    extra_context = {
        'form_title': 'Update Team Member',
        'submit_button_text': 'Update',
    }

    def get_success_url(self):
        return reverse("details_team_member", kwargs={"pk": self.object.pk})


class TeamMemberCardDeleteView(views.DeleteView):
    model = TeamMemberCard
    template_name = 'common/delete-team-member.html'


class AdvCardCreateView(views.CreateView):
    model = IndexPageAds
    fields = '__all__'
    template_name = 'shared_templates/form_template.html'
    extra_context = {
        'form_title': 'Create Advertisement',
        'submit_button_text': 'Create',
    }
    success_url = reverse_lazy('index')


class AdvCardUpdateView(views.UpdateView):
    model = IndexPageAds
    fields = '__all__'
    template_name = 'shared_templates/form_template.html'
    extra_context = {
        'form_title': 'Update Advertisement',
        'submit_button_text': 'Update',
    }
    success_url = reverse_lazy('index')


class AdvCardDeleteView(views.DeleteView):
    model = IndexPageAds
    template_name = 'common/delete-advertisement.html'
    success_url = reverse_lazy('index')


class ABoutMeDetailsView(views.DetailView):
    template_name = 'common/about.html'

    def get_object(self, queryset=None):
        return TeamMemberCard.objects.order_by('appearance_order', '-updated_at').first()


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')
