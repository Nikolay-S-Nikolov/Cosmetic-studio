from django import forms

from Cosmetic_studio.services.models import Services, ServicePricing, ServicePictures


class BaseServiceForm(forms.ModelForm):
    class Meta:
        model = Services
        fields = ['name', 'subheading', 'main_image', 'description']


class ServiceCreateForm(BaseServiceForm):
    pass


class ServiceUpdateForm(BaseServiceForm):
    pass


class BaseServicePricingForm(forms.ModelForm):
    class Meta:
        model = ServicePricing
        fields = ['service', 'service_type', 'treatment_description', 'price']


class ServicePricingCreateForm(BaseServicePricingForm):
    pass


class BaseServicePicturesForm(forms.ModelForm):
    class Meta:
        model = ServicePictures
        fields = ['service', 'image']


class ServicePicturesCreateForm(BaseServicePicturesForm):
    pass
