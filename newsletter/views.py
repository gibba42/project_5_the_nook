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
            "You're subscribed to The Nook newsletter."
        )
    else:
        for errors in form.errors.values():
            for error in errors:
                messages.error(request, error)

    return redirect(request.POST.get("next", "home"))