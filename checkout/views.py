from decimal import Decimal
import json

from django.conf import settings
from django.contrib import messages
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

import stripe

from bag.contexts import bag_contents
from profiles.forms import UserProfileForm
from profiles.models import UserProfile

from .forms import OrderForm
from .models import Order
from .services import (
    BasketValidationError,
    create_order_from_basket,
    validate_basket,
)


def _payment_intent_value(intent, field):
    """Read a Stripe object returned as an object or dictionary."""

    if isinstance(intent, dict):
        return intent.get(field)

    return getattr(intent, field, None)


@require_POST
def cache_checkout_data(request):
    """Attach the current basket and customer choices to Stripe metadata."""

    try:
        client_secret = request.POST.get("client_secret", "")
        pid = client_secret.split("_secret", 1)[0]

        if not pid:
            raise ValueError("Missing payment intent")

        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(
            pid,
            metadata={
                "bag": json.dumps(
                    request.session.get("bag", {}),
                    sort_keys=True,
                ),
                "save_info": request.POST.get(
                    "save_info",
                    "false",
                ),
                "username": (
                    request.user.get_username()
                    if request.user.is_authenticated
                    else "AnonymousUser"
                ),
            },
        )
        return HttpResponse(status=200)

    except Exception:
        messages.error(
            request,
            "Sorry, your payment cannot be processed right now. "
            "Please try again later.",
        )
        return HttpResponse(status=400)


def checkout(request):
    """Collect delivery details and complete a Stripe payment."""

    bag = request.session.get("bag", {})

    if not bag:
        messages.error(
            request,
            "There's nothing in your basket at the moment.",
        )
        return redirect("book_list")

    current_bag = bag_contents(request)
    expected_amount = int(
        (
            current_bag["grand_total"]
            * Decimal("100")
        ).quantize(Decimal("1"))
    )
    stripe.api_key = settings.STRIPE_SECRET_KEY

    if request.method == "POST":
        client_secret = request.POST.get("client_secret", "")
        pid = client_secret.split("_secret", 1)[0]

        if not pid:
            messages.error(
                request,
                "Payment details were missing. Please try again.",
            )
            return redirect("checkout")

        existing_order = Order.objects.filter(
            stripe_pid=pid
        ).first()

        try:
            intent = stripe.PaymentIntent.retrieve(pid)
        except Exception:
            messages.error(
                request,
                "We could not verify your payment. Please try again.",
            )
            return redirect("checkout")

        if (
            _payment_intent_value(intent, "status") != "succeeded"
            or _payment_intent_value(intent, "amount") != expected_amount
            or _payment_intent_value(intent, "currency")
            != settings.STRIPE_CURRENCY
            or _payment_intent_value(intent, "client_secret")
            != client_secret
        ):
            messages.error(
                request,
                "Your payment could not be verified. "
                "No order was created.",
            )
            return redirect("checkout")

        if existing_order:
            request.session["save_info"] = (
                "save-info" in request.POST
            )
            request.session["last_order_number"] = (
                existing_order.order_number
            )
            return redirect(
                "checkout_success",
                existing_order.order_number,
            )

        try:
            validate_basket(bag)
        except BasketValidationError as error:
            messages.error(request, str(error))
            return redirect("view_bag")

        order_form = OrderForm(request.POST)

        if order_form.is_valid():
            user_profile = None

            if request.user.is_authenticated:
                user_profile, _ = UserProfile.objects.get_or_create(
                    user=request.user
                )

            try:
                order, _ = create_order_from_basket(
                    bag=bag,
                    order_data=order_form.cleaned_data,
                    stripe_pid=pid,
                    user_profile=user_profile,
                )
            except BasketValidationError as error:
                messages.error(request, str(error))
                return redirect("view_bag")

            request.session["save_info"] = (
                "save-info" in request.POST
            )
            request.session["last_order_number"] = (
                order.order_number
            )

            return redirect(
                "checkout_success",
                order.order_number,
            )

        messages.error(
            request,
            "There was an error with your form. "
            "Please check your information and try again.",
        )
        client_secret = request.POST.get("client_secret", "")

    else:
        try:
            validate_basket(bag)
        except BasketValidationError as error:
            messages.error(request, str(error))
            return redirect("view_bag")

        if (
            not settings.STRIPE_PUBLIC_KEY
            or not settings.STRIPE_SECRET_KEY
        ):
            messages.error(
                request,
                "Checkout is not configured right now. "
                "Please try again later.",
            )
            return redirect("view_bag")

        try:
            intent = stripe.PaymentIntent.create(
                amount=expected_amount,
                currency=settings.STRIPE_CURRENCY,
            )
        except Exception:
            messages.error(
                request,
                "Checkout could not be started. "
                "Please try again later.",
            )
            return redirect("view_bag")

        client_secret = _payment_intent_value(
            intent,
            "client_secret",
        )

        if request.user.is_authenticated:
            profile, _ = UserProfile.objects.get_or_create(
                user=request.user
            )
            order_form = OrderForm(
                initial={
                    "full_name": profile.user.get_full_name(),
                    "email": profile.user.email,
                    "phone_number": profile.default_phone_number,
                    "country": profile.default_country,
                    "postcode": profile.default_postcode,
                    "town_or_city": profile.default_town_or_city,
                    "street_address1": (
                        profile.default_street_address1
                    ),
                    "street_address2": (
                        profile.default_street_address2
                    ),
                    "county": profile.default_county,
                }
            )
        else:
            order_form = OrderForm()

    context = {
        "order_form": order_form,
        "stripe_public_key": settings.STRIPE_PUBLIC_KEY,
        "client_secret": client_secret,
    }

    return render(
        request,
        "checkout/checkout.html",
        context,
    )


def checkout_success(request, order_number):
    """Show the completed order and clear the session basket."""

    order = get_object_or_404(
        Order,
        order_number=order_number,
    )
    session_order_number = request.session.get(
        "last_order_number"
    )

    if request.user.is_authenticated:
        profile, _ = UserProfile.objects.get_or_create(
            user=request.user
        )

        if order.user_profile not in (None, profile):
            raise Http404

        if (
            order.user_profile is None
            and session_order_number == order_number
        ):
            order.user_profile = profile
            order.save(update_fields=["user_profile"])

    elif session_order_number != order_number:
        raise Http404

    if (
        request.user.is_authenticated
        and request.session.get("save_info")
    ):
        profile_data = {
            "default_phone_number": order.phone_number,
            "default_country": order.country,
            "default_postcode": order.postcode,
            "default_town_or_city": order.town_or_city,
            "default_street_address1": order.street_address1,
            "default_street_address2": order.street_address2,
            "default_county": order.county,
        }
        user_profile_form = UserProfileForm(
            profile_data,
            instance=profile,
        )

        if user_profile_form.is_valid():
            user_profile_form.save()

    messages.success(
        request,
        f"Order successfully processed! Your order number is "
        f"{order_number}. A confirmation email will be sent "
        f"to {order.email}.",
    )

    request.session.pop("bag", None)
    request.session.pop("save_info", None)

    return render(
        request,
        "checkout/checkout_success.html",
        {"order": order},
    )