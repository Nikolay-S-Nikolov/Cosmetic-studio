from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic as views

from Cosmetic_studio.services.forms import ServiceCreateForm, ServicePricingCreateForm, ServicePicturesCreateForm, \
    ServiceUpdateForm, ServicePricingUpdateForm
from Cosmetic_studio.services.models import Services, ServicePricing, ServicePictures


class ServicesView(views.ListView):
    model = Services
    template_name = 'services/list_services.html'


class CreateServiceView(views.CreateView):
    form_class = ServiceCreateForm
    template_name = 'services/create_service.html'
    success_url = reverse_lazy('services')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class UpdateServiceView(views.UpdateView):
    model = Services
    form_class = ServiceUpdateForm
    template_name = 'services/update_service.html'

    def get_success_url(self):
        return reverse_lazy('details_service', kwargs={'pk': self.object.pk})


class DeleteServiceView(views.DeleteView):
    model = Services
    template_name = 'services/delete_service.html'
    success_url = reverse_lazy('services')


class ServiceDetailsView(views.DetailView):
    model = Services
    template_name = 'services/service_details.html'


class CreateServicePricingView(views.CreateView):
    form_class = ServicePricingCreateForm
    template_name = 'services/create_pricing.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('details_service', kwargs={'pk': self.object.service.pk})


class UpdatePricingView(views.UpdateView):
    model = ServicePricing
    form_class = ServicePricingUpdateForm
    template_name = 'services/update_pricing.html'

    def get_success_url(self):
        return reverse_lazy('details_service', kwargs={'pk': self.object.service.pk})


class DeletePricingView(views.DeleteView):
    model = ServicePricing

    def get_success_url(self):
        return reverse_lazy('details_service', kwargs={'pk': self.object.service.pk})


class CreateServicePicturesView(views.CreateView):
    form_class = ServicePicturesCreateForm
    template_name = 'services/create_pictures.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('details_service', kwargs={'pk': self.object.service.pk})


class DeleteServicePicturesView(views.DeleteView):
    model = ServicePictures

    def get_success_url(self):
        return reverse_lazy('details_service', kwargs={'pk': self.object.service.pk})
