import json
import time

from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse
from django.template.loader import render_to_string

import stripe

from profiles.models import UserProfile

from .models import Order
from .services import (
    BasketValidationError,
    create_order_from_basket,
)


class StripeWH_Handler:
    """Handle the Stripe events used by The Nook checkout."""

    def __init__(self, request):
        self.request = request

    def _send_confirmation_email(self, order):
        subject = render_to_string(
            (
                "checkout/confirmation_emails/"
                "confirmation_email_subject.txt"
            ),
            {"order": order},
        ).strip()
        body = render_to_string(
            (
                "checkout/confirmation_emails/"
                "confirmation_email_body.txt"
            ),
            {
                "order": order,
                "contact_email": settings.DEFAULT_FROM_EMAIL,
            },
        )
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [order.email],
        )

    def handle_event(self, event):
        return HttpResponse(
            content=(
                f'Unhandled webhook received: {event["type"]}'
            ),
            status=200,
        )

    def handle_payment_intent_succeeded(self, event):
        """Verify an order exists, creating it if necessary."""

        intent = event["data"]["object"]
        pid = intent["id"]
        metadata = intent.get("metadata", {})

        for _ in range(5):
            existing_order = Order.objects.filter(
                stripe_pid=pid
            ).first()

            if existing_order:
                self._send_confirmation_email(existing_order)
                return HttpResponse(
                    content=(
                        f'Webhook received: {event["type"]} | '
                        "SUCCESS: Verified existing order"
                    ),
                    status=200,
                )

            time.sleep(1)

        try:
            bag = json.loads(metadata.get("bag", "{}"))
            shipping = intent["shipping"]
            address = shipping["address"]
            payment_method = stripe.PaymentMethod.retrieve(
                intent["payment_method"]
            )
            billing_details = payment_method["billing_details"]

            username = metadata.get(
                "username",
                "AnonymousUser",
            )
            profile = None

            if username != "AnonymousUser":
                profile = UserProfile.objects.filter(
                    user__username=username
                ).first()

            order_data = {
                "full_name": shipping["name"],
                "email": billing_details["email"],
                "phone_number": shipping["phone"],
                "country": address["country"],
                "postcode": address.get("postal_code") or "",
                "town_or_city": address["city"],
                "street_address1": address["line1"],
                "street_address2": address.get("line2") or "",
                "county": address.get("state") or "",
            }

            order, _ = create_order_from_basket(
                bag=bag,
                order_data=order_data,
                stripe_pid=pid,
                user_profile=profile,
            )

            save_info = (
                str(
                    metadata.get("save_info", "false")
                ).lower()
                == "true"
            )

            if profile and save_info:
                profile.default_phone_number = (
                    order.phone_number
                )
                profile.default_country = order.country
                profile.default_postcode = order.postcode
                profile.default_town_or_city = (
                    order.town_or_city
                )
                profile.default_street_address1 = (
                    order.street_address1
                )
                profile.default_street_address2 = (
                    order.street_address2
                )
                profile.default_county = order.county
                profile.save()

        except (
            BasketValidationError,
            KeyError,
            TypeError,
            ValueError,
        ) as error:
            return HttpResponse(
                content=(
                    f'Webhook received: {event["type"]} | '
                    f"ERROR: {error}"
                ),
                status=500,
            )

        except Exception as error:
            return HttpResponse(
                content=(
                    f'Webhook received: {event["type"]} | '
                    f"ERROR: {error}"
                ),
                status=500,
            )

        self._send_confirmation_email(order)

        return HttpResponse(
            content=(
                f'Webhook received: {event["type"]} | '
                "SUCCESS: Created order"
            ),
            status=200,
        )

    def handle_payment_intent_payment_failed(self, event):
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200,
        )
