from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Account

import re


class Registration_form(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Account
        fields = ['username', 'first_name', 'last_name', 'email',
                  'phone_number', 'password', 'confirm_password']

    # Applying custom settings to form widgets is used when creating an instance of the form class.
    def __init__(self, *args, **kwargs):
        super(Registration_form, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'input_second input_all'

    # check the password == confirm_password

    def clean(self):
        cleaned_data = super(Registration_form, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        phone_number = cleaned_data.get('phone_number')
        if password != confirm_password:
            raise forms.ValidationError("پسوورد مطابقت ندارد !")
        pattern = re.compile(r'^(09\d{9}|9\d{9})$')
        if not pattern.match(phone_number):
            raise forms.ValidationError(
                "شماره تلفن همراه نامعتبر است. شماره باید با '09' شروع شود و ۱۱ رقمی باشد.")

        if Account.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError(
                "این شماره تلفن همراه قبلاً ثبت شده است.")
