"""Services for integrating newsletter subscriptions with Mailchimp."""

import hashlib
import logging

import requests
from django.conf import settings


logger = logging.getLogger(__name__)


class MailchimpError(Exception):
    """Raised when a Mailchimp subscription request fails."""


def subscribe_to_mailchimp(email):
    """Add or update an email address in the Mailchimp audience."""

    api_key = settings.MAILCHIMP_API_KEY
    server_prefix = settings.MAILCHIMP_SERVER_PREFIX
    audience_id = settings.MAILCHIMP_AUDIENCE_ID

    if not all((api_key, server_prefix, audience_id)):
        logger.error("Mailchimp environment variables are not configured.")
        raise MailchimpError

    normalized_email = email.strip().lower()

    subscriber_hash = hashlib.md5(
        normalized_email.encode("utf-8")
    ).hexdigest()

    url = (
        f"https://{server_prefix}.api.mailchimp.com/3.0/"
        f"lists/{audience_id}/members/{subscriber_hash}"
    )

    try:
        response = requests.put(
            url,
            auth=("thenook", api_key),
            json={
                "email_address": normalized_email,
                "status_if_new": "subscribed",
            },
            timeout=10,
        )

        response.raise_for_status()

    except requests.RequestException as error:
        logger.exception(
            "Mailchimp subscription failed for %s",
            normalized_email,
        )
        raise MailchimpError from error

    return response.json()