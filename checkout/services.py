import json

from django.db import transaction

from books.models import Book

from .models import Order, OrderLineItem


class BasketValidationError(Exception):
    """Raised when a basket can no longer be fulfilled."""


def validate_basket(bag, *, lock=False):
    """Return purchasable books and quantities from a session basket."""

    try:
        book_ids = [int(item_id) for item_id in bag]
    except (TypeError, ValueError):
        raise BasketValidationError("Your basket contains an invalid item.")

    queryset = Book.objects.filter(
        pk__in=book_ids,
        is_active=True,
        status=Book.Status.APPROVED,
    )
    if lock:
        queryset = queryset.select_for_update()

    books = {str(book.pk): book for book in queryset}
    items = []

    for item_id, raw_quantity in bag.items():
        book = books.get(str(item_id))
        if book is None:
            raise BasketValidationError(
                "A book in your basket is no longer available."
            )

        try:
            quantity = int(raw_quantity)
        except (TypeError, ValueError):
            raise BasketValidationError(
                "Your basket contains an invalid quantity."
            )

        if quantity < 1:
            raise BasketValidationError(
                "Book quantities must be at least one."
            )
        if quantity > book.stock_quantity:
            raise BasketValidationError(
                f"Only {book.stock_quantity} copies of "
                f"{book.title} are available."
            )

        items.append((book, quantity))

    if not items:
        raise BasketValidationError("Your basket is empty.")

    return items


def create_order_from_basket(
    *,
    bag,
    order_data,
    stripe_pid,
    user_profile=None,
):
    """Create one order, its line items, and reduce stock atomically."""

    with transaction.atomic():
        existing_order = Order.objects.filter(
            stripe_pid=stripe_pid
        ).first()

        if existing_order:
            return existing_order, False

        items = validate_basket(bag, lock=True)
        order = Order.objects.create(
            **order_data,
            user_profile=user_profile,
            original_bag=json.dumps(bag, sort_keys=True),
            stripe_pid=stripe_pid,
        )

        for book, quantity in items:
            OrderLineItem.objects.create(
                order=order,
                book=book,
                quantity=quantity,
            )
            book.stock_quantity -= quantity
            book.save(update_fields=["stock_quantity"])

    return order, True