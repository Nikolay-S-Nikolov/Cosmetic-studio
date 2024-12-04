import asyncio
import time

from django.shortcuts import render
from django.views import View
from django.contrib.messages import views as message_views
from django.urls import reverse_lazy
from django.views import generic as views
from Cosmetic_studio import settings
from Cosmetic_studio.blog.models import BlogContent, Tag
from Cosmetic_studio.contact.forms import ContactForm
from Cosmetic_studio.contact.models import ContactInfo
from Cosmetic_studio.utils.my_email import send_simple_email_async


class ContactPageInfo(message_views.SuccessMessageMixin, views.FormView):
    template_name = 'contact/contact_info.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact_success')

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
        context['random_list'] = BlogContent.objects.order_by('?')[:2]
        context['tags_list'] = Tag.objects.order_by('name')
        return context


class ContactSuccessPageInfo(message_views.SuccessMessageMixin, views.TemplateView):
    template_name = 'contact/contact_success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['async_time'] = self.request.session.get('async_time', 'N/A')
        context['sync_time'] = self.request.session.get('sync_time', 'N/A')
        return context


class AsyncEmailView(View):
    form_class = ContactForm
    success_message = 'Thank you for your message. We will get back to you shortly.'

    async def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            start_time = time.time()  # Start time
            await self.form_valid(form)
            end_time = time.time()  # End time
            async_time = end_time - start_time  # Calculate total time
            self.request.session['async_time'] = async_time  # Store in session
            return render(
                request,
                'contact/contact_success.html',
                {'message': self.success_message, 'async_time': async_time}
            )
        else:
            return render(request, 'contact/contact_info.html', {'form': form, 'errors': form.errors})

    async def form_valid(self, form):
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        message = form.cleaned_data['message']

        subject = f'New message from {name} ({email})'
        email_message = f'Name: {name}\nEmail: {email}\nMessage:\n{message}'

        await self.send_emails_async(subject, email_message)

    @staticmethod
    async def send_emails_async(subject, message):
        await asyncio.gather(
            send_simple_email_async(subject, message, [settings.MY_EMAIL]),
            send_simple_email_async(subject, message, [settings.MY_EMAIL]),
            send_simple_email_async(subject, message, [settings.MY_EMAIL]),
        )

# for testing purposes

# import asyncio
# import time
#
# from asgiref.sync import async_to_sync
# from django.contrib.messages import views as message_views
# from django.urls import reverse_lazy
# from django.views import generic as views
# from Cosmetic_studio import settings
# from Cosmetic_studio.blog.models import BlogContent, Tag
# from Cosmetic_studio.contact.forms import ContactForm
# from Cosmetic_studio.contact.models import ContactInfo
# from Cosmetic_studio.utils.my_email import send_simple_email, send_simple_email_sync
#
#
# class ContactPageInfo(message_views.SuccessMessageMixin, views.FormView):
#     template_name = 'contact/contact_info.html'
#     form_class = ContactForm
#     success_url = reverse_lazy('contact_success')
#     success_message = 'Thank you for your message. We will get back to you shortly.'
#
#     def get_initial(self):
#         initial = super().get_initial()
#         if self.request.user.is_authenticated:
#             name = self.request.user.profile.get_profile_name() if not 'Anonymous' else ''
#             initial.update({
#                 'name': name,
#                 'email': self.request.user.email,
#                 'phone': self.request.user.profile.phone_number
#             })
#         return initial
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['object'] = ContactInfo.objects.filter(visible=True).order_by('-created_at').first()
#         context['random_list'] = BlogContent.objects.order_by('?')[:2]
#         context['tags_list'] = Tag.objects.order_by('name')
#         return context
#
#     def form_valid(self, form):
#         name = form.cleaned_data['name']
#         email = form.cleaned_data['email']
#         message = form.cleaned_data['message']
#
#         subject = f'New message from {name} ({email})'
#         email_message = f'Name: {name}\nEmail: {email}\nMessage:\n{message}'
#
#         start_time = time.time()
#         async_to_sync(self.send_emails_async)(subject, email_message)
#         async_time = time.time() - start_time
#
#         # Test synchronous email sending
#         start_time = time.time()
#         self.send_emails_sync(subject, email_message)
#         sync_time = time.time() - start_time
#
#         self.request.session['async_time'] = async_time
#         self.request.session['sync_time'] = sync_time
#
#         return super().form_valid(form)
#
#     @staticmethod
#     async def send_emails_async(subject, message):
#         await asyncio.gather(
#             send_simple_email(subject, message, [settings.MY_EMAIL]),
#             send_simple_email(subject, message, [settings.MY_EMAIL]),
#             send_simple_email(subject, message, [settings.MY_EMAIL]),
#         )
#
#     @staticmethod
#     def send_emails_sync(subject, message):
#         send_simple_email_sync(subject, message, [settings.MY_EMAIL])
#         send_simple_email_sync(subject, message, [settings.MY_EMAIL])
#         send_simple_email_sync(subject, message, [settings.MY_EMAIL])
#
#
# class ContactSuccessPageInfo(views.TemplateView):
#     template_name = 'contact/contact_success.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['async_time'] = self.request.session.get('async_time', 'N/A')
#         context['sync_time'] = self.request.session.get('sync_time', 'N/A')
#         return context
