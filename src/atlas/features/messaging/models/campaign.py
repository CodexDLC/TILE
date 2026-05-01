from codex_django.messaging import AbstractCampaign, AbstractCampaignRecipient
from django.db import models


def _(message: str) -> str:
    return message


class Campaign(AbstractCampaign):
    class Meta:
        verbose_name = _("Campaign")
        verbose_name_plural = _("Campaigns")


class CampaignRecipient(AbstractCampaignRecipient):
    campaign = models.ForeignKey(
        "messaging.Campaign",
        on_delete=models.CASCADE,
        related_name="recipients",
    )

    class Meta:
        verbose_name = _("Campaign recipient")
        verbose_name_plural = _("Campaign recipients")
