from typing import ClassVar

from django import forms
from django.utils.translation import gettext_lazy as _

from ..models import Message, Thread


class ContactForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields: ClassVar[list[str]] = ["sender_name", "sender_email", "sender_phone", "subject", "topic"]
        labels: ClassVar[dict[str, str]] = {
            "sender_name": _("Your Name"),
            "sender_email": _("Your Email"),
            "sender_phone": _("Phone (optional)"),
            "subject": _("Subject"),
            "topic": _("Topic"),
        }
        widgets: ClassVar[dict[str, forms.Widget]] = {
            "sender_phone": forms.TextInput(attrs={"placeholder": _("+49 ...")}),
        }

    body = forms.CharField(label=_("Message"), widget=forms.Textarea(attrs={"rows": 5}))

    def save(self, commit: bool = True) -> Thread:
        thread = super().save(commit=False)
        thread.source = "contact_form"
        thread.channel = "email"
        thread.status = Thread.Status.OPEN
        if commit:
            thread.save()
            Message.objects.create(
                thread=thread,
                direction=Message.Direction.INBOUND,
                sender_name=thread.sender_name,
                sender_email=thread.sender_email,
                subject=thread.subject,
                body=self.cleaned_data["body"],
                source=thread.source,
                channel=thread.channel,
            )
        return thread


