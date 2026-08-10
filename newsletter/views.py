"""Views for newsletter subscriptions."""

from django.contrib import messages
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

from .forms import NewsletterSignupForm


@require_POST
def newsletter_signup(request):
    """Subscribe a visitor to The Nook newsletter."""

    form = NewsletterSignupForm(request.POST)

    if form.is_valid():
        form.save()

        messages.success(
            request,
            "Thanks for subscribing to The Nook newsletter!"
        )
    else:
        if "email" in form.errors:
            for error in form.errors["email"]:
                messages.error(request, error)
        else:
            messages.error(
                request,
                "We couldn't complete your newsletter signup. "
                "Please check your details and try again."
            )

    return redirect(request.POST.get("next", "home"))