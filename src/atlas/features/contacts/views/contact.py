from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.views.generic import FormView

from features.contacts.forms import ContactForm
from features.contacts.services import send_inquiry


class ContactView(FormView):
    template_name = "contacts/contact.html"
    form_class = ContactForm

    def form_valid(self, form):
        send_inquiry(**form.cleaned_data)
        messages.success(self.request, _("Thank you. Your message has been sent."))
        return redirect("contacts")
