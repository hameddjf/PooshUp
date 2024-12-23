from email_validator import validate_email, EmailNotValidError
import re
from django import forms
from django.core.validators import RegexValidator
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone',
                  'email', 'address_line_1', 'postal_code',
                  'state', 'city', 'street', 'tag']
