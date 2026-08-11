from decimal import Decimal

from django.conf import settings

from books.models import Book


def bag_contents(request):
    """Make basket books and totals available to every template."""

    bag_items = []
    total = Decimal("0.00")
    book_count = 0
    bag = request.session.get("bag", {})
    cleaned_bag = {}

    for item_id, quantity in bag.items():
        try:
            quantity = int(quantity)
        except (TypeError, ValueError):
            continue

        book = Book.objects.filter(
            pk=item_id,
            is_active=True,
            status=Book.Status.APPROVED,
        ).first()

        if book is None or quantity < 1:
            continue

        cleaned_bag[str(item_id)] = quantity
        total += quantity * book.price
        book_count += quantity
        bag_items.append({
            "item_id": str(item_id),
            "quantity": quantity,
            "book": book,
        })

    if cleaned_bag != bag:
        request.session["bag"] = cleaned_bag

    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery_percentage = (
            Decimal(settings.STANDARD_DELIVERY_PERCENTAGE) / Decimal("100")
        )
        delivery = total * delivery_percentage
        free_delivery_delta = Decimal(settings.FREE_DELIVERY_THRESHOLD) - total
    else:
        delivery = Decimal("0.00")
        free_delivery_delta = Decimal("0.00")

    grand_total = delivery + total

    return {
        "bag_items": bag_items,
        "total": total,
        "book_count": book_count,
        "delivery": delivery,
        "free_delivery_delta": free_delivery_delta,
        "free_delivery_threshold": settings.FREE_DELIVERY_THRESHOLD,
        "grand_total": grand_total,
    }
