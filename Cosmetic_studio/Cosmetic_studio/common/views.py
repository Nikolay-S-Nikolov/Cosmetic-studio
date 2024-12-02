from django.urls import reverse_lazy, reverse
from django.views import generic as views
from Cosmetic_studio.blog.models import BlogContent, Tag
from Cosmetic_studio.common.models import TeamMemberCard, IndexPageAds
from Cosmetic_studio.services.models import Services
from Cosmetic_studio.utils.common_mixins import StaffRequiredMixin, CommonMessageMixin


class IndexView(views.ListView):
    model = TeamMemberCard
    template_name = 'common/index.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ads'] = IndexPageAds.objects.all().order_by("-created_at")[:2]
        context['footer_services'] = Services.objects.order_by("-created_at")[:4]
        context['random_list'] = BlogContent.objects.order_by('?')[:2]
        context['tags_list'] = Tag.objects.order_by('name')
        return context


class TeamMemberDetailsView(views.DetailView):
    model = TeamMemberCard
    template_name = 'common/team-member-details.html'


class TeamMemberCardCreateView(CommonMessageMixin, StaffRequiredMixin, views.CreateView):
    model = TeamMemberCard
    fields = [
        'name',
        'picture',
        'featured_image',
        'about_image',
        'title',
        'description',
        'role',
        'specialities',
        'is_active',
        'appearance_order',
    ]
    template_name = 'shared_templates/form_template.html'
    extra_context = {
        'form_title': 'Add Team Member',
        'submit_button_text': 'Add',
    }
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class TeamMemberCardUpdateView(CommonMessageMixin, StaffRequiredMixin, views.UpdateView):
    model = TeamMemberCard
    fields = [
        'name',
        'picture',
        'featured_image',
        'about_image',
        'title',
        'description',
        'role',
        'specialities',
        'is_active',
        'appearance_order',
    ]
    template_name = 'shared_templates/form_template.html'
    extra_context = {
        'form_title': 'Update Team Member',
        'submit_button_text': 'Update',
    }

    def get_success_url(self):
        return reverse("details_team_member", kwargs={"pk": self.object.pk})


class TeamMemberCardDeleteView(CommonMessageMixin,StaffRequiredMixin, views.DeleteView):
    model = TeamMemberCard
    template_name = 'common/delete-team-member.html'
    success_url = reverse_lazy('index')


class AdvCardCreateView(CommonMessageMixin,StaffRequiredMixin, views.CreateView):
    model = IndexPageAds
    fields = [
        'name',
        'adv_description',
        'adv_link',
        'adv_image'
    ]
    template_name = 'shared_templates/form_template.html'
    extra_context = {
        'form_title': 'Create Advertisement',
        'submit_button_text': 'Create',
    }
    success_url = reverse_lazy('index')
    object_name = 'Advertisement'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class AdvCardUpdateView(CommonMessageMixin,StaffRequiredMixin, views.UpdateView):
    model = IndexPageAds
    fields = [
        'name',
        'adv_description',
        'adv_link',
        'adv_image'
    ]
    template_name = 'shared_templates/form_template.html'
    extra_context = {
        'form_title': 'Update Advertisement',
        'submit_button_text': 'Update',
    }
    success_url = reverse_lazy('index')
    object_name = 'Advertisement'


class AdvCardDeleteView(CommonMessageMixin,StaffRequiredMixin, views.DeleteView):
    model = IndexPageAds
    template_name = 'common/delete-advertisement.html'
    success_url = reverse_lazy('index')
    object_name = 'Advertisement'


class ABoutMeDetailsView(views.DetailView):
    template_name = 'common/about.html'
    extra_context = {
        'footer_services': Services.objects.order_by("-created_at")[:4]
    }

    def get_object(self, queryset=None):
        return TeamMemberCard.objects.order_by('appearance_order', '-updated_at').first()
