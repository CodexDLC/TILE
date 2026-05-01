from django import forms
from django.utils.translation import gettext_lazy as _


class ContactForm(forms.Form):
    name = forms.CharField(label=_("Name"), max_length=255)
    email = forms.EmailField(label=_("Email"))
    topic = forms.CharField(label=_("Topic"), max_length=255, required=False)
    message = forms.CharField(label=_("Message"), widget=forms.Textarea)
