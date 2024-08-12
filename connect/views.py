import hashlib

from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import FormView, CreateView
from django.views import View
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.utils.html import format_html

from accounts.models import Account

from .models import ContactPage


class ContactView(CreateView):
    model = ContactPage
    fields = ['name', 'email', 'title', 'message']
    template_name = 'contact.html'
    success_url = '/'

    def form_valid(self, form):
        print("Form data:", form.cleaned_data)
        return super().form_valid(form)
# api_key = 'AIzaSyDD4Q3_bDRaTyVw7clCwijbSna4HANUPsY'


class CreatorView(ListView):
    model = Account
    template_name = 'creators.html'
    context_object_name = 'creators'

    def get_queryset(self):
        # فقط کاربرانی که is_superadmin=True هستند را برمی‌گرداند
        return self.model.objects.filter(is_superadmin=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_gravatar_url(self, email, size=100):
        email_hash = hashlib.md5(email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{email_hash}?s={size}&d=identicon'

    def get_profile_image(self, user):
        # برای دریافت تصویر پروفایل از Gravatar با استفاده از ایمیل
        return self.get_gravatar_url(user.email)


# class AboutView(TemplateView):
#     template_name = 'about.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['about_page'] = AboutPage.objects.first()
#         return context
