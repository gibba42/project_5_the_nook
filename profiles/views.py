from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from authors.models import AuthorProfile
from checkout.models import Order

from .forms import UserProfileForm
from .models import UserProfile


@login_required
def profile(request):
    """Display and update the signed-in user's account profile."""

    user_profile = get_object_or_404(
        UserProfile,
        user=request.user,
    )

    if request.method == "POST":
        form = UserProfileForm(
            request.POST,
            instance=user_profile,
        )

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Your delivery details have been updated.",
            )
            return redirect("profile")

        messages.error(
            request,
            "We could not update your details. "
            "Please check the form and try again.",
        )
    else:
        form = UserProfileForm(instance=user_profile)

    orders = (
        user_profile.orders
        .prefetch_related("lineitems__product")
        .order_by("-date")
    )

    try:
        author_profile = request.user.author_profile
    except AuthorProfile.DoesNotExist:
        author_profile = None

    context = {
        "form": form,
        "orders": orders,
        "author_profile": author_profile,
        "on_profile_page": True,
    }

    return render(
        request,
        "profiles/profile.html",
        context,
    )


@login_required
def order_history(request, order_number):
    """Show an order belonging to the signed-in user."""

    order = get_object_or_404(
        Order,
        order_number=order_number,
        user_profile=request.user.userprofile,
    )

    messages.info(
        request,
        f"This is a previous order confirmation for "
        f"{order_number}. A confirmation email was sent "
        f"when the order was placed.",
    )

    context = {
        "order": order,
        "from_profile": True,
    }

    return render(
        request,
        "checkout/checkout_success.html",
        context,
    )