from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic as views

from Cosmetic_studio.services.forms import ServiceCreateForm, ServicePricingCreateForm, ServicePicturesCreateForm
from Cosmetic_studio.services.models import Services


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


class ServiceDetailsView(views.DetailView):
    model = Services
    template_name = 'services/service_details.html'


class CreateServicePricingView(views.CreateView):
    form_class = ServicePricingCreateForm
    template_name = 'services/create_pricing.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class CreateServicePicturesView(views.CreateView):
    form_class = ServicePicturesCreateForm
    template_name = 'services/create_pictures.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
