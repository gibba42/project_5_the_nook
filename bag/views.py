from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from books.models import Book


def view_bag(request):
    """Render the current basket."""

    return render(request, "bag/bag.html")


def _basket_redirect(request, fallback):
    """Return only a local redirect supplied by one of our own forms."""

    redirect_url = request.POST.get("redirect_url")
    if redirect_url and url_has_allowed_host_and_scheme(
        url=redirect_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return redirect_url
    return fallback


def _quantity_from_post(request):
    """Parse a positive integer quantity, returning ``None`` if invalid."""

    try:
        quantity = int(request.POST.get("quantity", "1"))
    except (TypeError, ValueError):
        return None
    return quantity if quantity > 0 else None


@require_POST
def add_to_bag(request, item_id):
    """Add an approved, active book to the session basket."""

    book = get_object_or_404(
        Book,
        pk=item_id,
        is_active=True,
        status=Book.Status.APPROVED,
    )
    fallback = reverse("book_detail", args=[book.pk])
    redirect_url = _basket_redirect(request, fallback)
    quantity = _quantity_from_post(request)

    if quantity is None:
        messages.error(request, "Please choose a valid quantity.")
        return redirect(redirect_url)

    bag = request.session.get("bag", {})
    item_key = str(item_id)
    new_quantity = bag.get(item_key, 0) + quantity

    if new_quantity > book.stock_quantity:
        messages.error(
            request,
            f"Only {book.stock_quantity} copies of {book.title} are available.",
        )
        return redirect(redirect_url)

    bag[item_key] = new_quantity
    request.session["bag"] = bag
    messages.success(request, f"Added {book.title} to your basket.", extra_tags="basket-add")
    return redirect(redirect_url)


@require_POST
def adjust_bag(request, item_id):
    """Set the quantity for a book already in the basket."""

    book = get_object_or_404(
        Book,
        pk=item_id,
        is_active=True,
        status=Book.Status.APPROVED,
    )
    quantity = _quantity_from_post(request)
    bag = request.session.get("bag", {})
    item_key = str(item_id)

    if item_key not in bag:
        messages.error(request, f"{book.title} is not in your basket.")
    elif quantity is None:
        messages.error(request, "Please choose a valid quantity.")
    elif quantity > book.stock_quantity:
        messages.error(
            request,
            f"Only {book.stock_quantity} copies of {book.title} are available.",
        )
    else:
        bag[item_key] = quantity
        request.session["bag"] = bag
        messages.success(request, f"Updated {book.title} quantity to {quantity}.",extra_tags="basket-update")

    return redirect("view_bag")


@require_POST
def remove_from_bag(request, item_id):
    """Remove a book from the basket."""

    book = get_object_or_404(Book, pk=item_id)
    bag = request.session.get("bag", {})
    item_key = str(item_id)

    if item_key in bag:
        bag.pop(item_key)
        request.session["bag"] = bag
        messages.success(request, f"Removed {book.title} from your basket.",extra_tags="basket-remove")

    return redirect("view_bag")