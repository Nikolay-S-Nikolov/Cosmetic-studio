from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic as views

from Cosmetic_studio.services.forms import ServiceCreateForm, ServicePricingCreateForm, ServicePicturesCreateForm, \
    ServiceUpdateForm, ServicePricingUpdateForm
from Cosmetic_studio.services.models import Services, ServicePricing, ServicePictures


# TODO implement user permissions and access control
class ServicesView(views.ListView):
    model = Services
    template_name = 'services/list_services.html'


class CreateServiceView(views.CreateView):
    form_class = ServiceCreateForm
    template_name = 'shared_templates/form_template.html'
    extra_context = {
        'form_title': 'Create Service',
        'submit_button_text': 'Create',
    }
    success_url = reverse_lazy('services')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class UpdateServiceView(views.UpdateView):
    model = Services
    form_class = ServiceUpdateForm
    template_name = 'shared_templates/form_template.html'
    extra_context = {
        'form_title': 'Update Service',
        'submit_button_text': 'Update',
    }

    def get_success_url(self):
        return reverse_lazy('details_service', kwargs={'pk': self.object.pk})


class DeleteServiceView(views.DeleteView):
    model = Services
    template_name = 'services/delete_service.html'
    success_url = reverse_lazy('services')


class ServiceDetailsView(views.DetailView):
    model = Services
    template_name = 'services/service_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['footer_services'] = Services.objects.order_by("?")[:4]
        return context


class CreateServicePricingView(views.CreateView):
    form_class = ServicePricingCreateForm
    template_name = 'shared_templates/form_template.html'
    extra_context = {
        'form_title': 'Create Pricing',
        'submit_button_text': 'Create',
    }

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('details_service', kwargs={'pk': self.object.service.pk})


class UpdatePricingView(views.UpdateView):
    model = ServicePricing
    form_class = ServicePricingUpdateForm
    template_name = 'shared_templates/form_template.html'
    extra_context = {
        'form_title': 'Update Pricing',
        'submit_button_text': 'Update',
    }

    def get_success_url(self):
        return reverse_lazy('details_service', kwargs={'pk': self.object.service.pk})


class DeletePricingView(views.DeleteView):
    model = ServicePricing

    def get_success_url(self):
        return reverse_lazy('details_service', kwargs={'pk': self.object.service.pk})


class CreateServicePicturesView(views.CreateView):
    form_class = ServicePicturesCreateForm
    template_name = 'shared_templates/form_template.html'
    extra_context = {
        'form_title': 'Upload Picture',
        'submit_button_text': 'Upload',
    }

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('details_service', kwargs={'pk': self.object.service.pk})


class DeleteServicePicturesView(views.DeleteView):
    model = ServicePictures

    def get_success_url(self):
        return reverse_lazy('details_service', kwargs={'pk': self.object.service.pk})
