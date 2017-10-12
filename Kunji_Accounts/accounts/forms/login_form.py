import logging
import re

from django import forms

logger = logging.getLogger(__name__)
password_regex = re.compile(r'^.*(?=.{8,}).*$')


class LoginForm(forms.Form):
    use_required_attribute = False
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Work Email Address', 'tabindex': '1',
                                      'class': 'w-input form-field dark',
                                      "name": "Field", "data-name": "Field",}), label='')
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'tabindex': '2',
                                          'class': 'w-input form-field dark',
                                          'name': "Field", 'data-name': "Field"}), label='')
