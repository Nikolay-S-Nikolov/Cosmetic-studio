from django.contrib.messages import views as message_views
from django.urls import reverse_lazy
from django.views import generic as views

from Cosmetic_studio import settings
from Cosmetic_studio.contact.forms import ContactForm
from Cosmetic_studio.contact.models import ContactInfo
from Cosmetic_studio.utils.my_email import send_simple_email


class ContactPageInfo(message_views.SuccessMessageMixin, views.FormView):
    template_name = 'contact/contact_info.html'
    form_class = ContactForm
    success_url = reverse_lazy('index')
    success_message = 'Thank you for your message. We will get back to you shortly.'

    def get_initial(self):
        initial = super().get_initial()
        if self.request.user.is_authenticated:
            name = self.request.user.profile.get_profile_name() if not 'Anonymous' else ''
            initial.update({
                'name': name,
                'email': self.request.user.email,
                'phone': self.request.user.profile.phone_number
            })
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = ContactInfo.objects.filter(visible=True).order_by('-created_at').first()
        return context

    def form_valid(self, form):
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        message = form.cleaned_data['message']

        subject = f'New message from {name} ({email})'
        email_message = f'Name: {name}\nEmail: {email}\nMessage:\n{message}'

        send_simple_email(subject=subject, message=email_message, recipient_list=[settings.MY_EMAIL] )

        return super().form_valid(form)
