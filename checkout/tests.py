from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import patch

from django.test import TestCase, override_settings
from django.urls import reverse

from authors.models import AuthorProfile
from books.models import Book

from .models import Order


@override_settings(
    STRIPE_PUBLIC_KEY="pk_test_example",
    STRIPE_SECRET_KEY="sk_test_example",
    STRIPE_CURRENCY="gbp",
)
class CheckoutViewTests(TestCase):
    def setUp(self):
        author = AuthorProfile.objects.create(display_name="Elin Moss")
        self.book = Book.objects.create(
            author=author,
            title="Salt & Hawthorn",
            description="A test book.",
            price=Decimal("10.00"),
            stock_quantity=5,
            status=Book.Status.APPROVED,
        )
        self.checkout_data = {
            "full_name": "Jamie Reader",
            "email": "jamie@example.com",
            "phone_number": "07123456789",
            "country": "GB",
            "postcode": "SW1A 1AA",
            "town_or_city": "London",
            "street_address1": "1 Book Lane",
            "street_address2": "",
            "county": "Greater London",
            "client_secret": "pi_test_order_secret_example",
        }

    def put_book_in_basket(self, quantity=1):
        session = self.client.session
        session["bag"] = {str(self.book.pk): quantity}
        session.save()

    def successful_intent(self):
        return SimpleNamespace(
            status="succeeded",
            amount=1100,
            currency="gbp",
            client_secret="pi_test_order_secret_example",
        )

    def test_empty_basket_redirects_to_catalogue(self):
        response = self.client.get(reverse("checkout"))

        self.assertRedirects(response, reverse("book_list"))

    @patch("checkout.views.stripe.PaymentIntent.create")
    def test_checkout_displays_book_summary(self, create_intent):
        create_intent.return_value = SimpleNamespace(
            client_secret="pi_test_order_secret_example"
        )
        self.put_book_in_basket()

        response = self.client.get(reverse("checkout"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Salt &amp; Hawthorn")
        self.assertContains(response, "£11.00")
        create_intent.assert_called_once_with(
            amount=1100,
            currency="gbp",
        )

    @patch("checkout.views.stripe.PaymentIntent.retrieve")
    def test_successful_checkout_creates_book_order_and_reduces_stock(
        self,
        retrieve_intent,
    ):
        retrieve_intent.return_value = self.successful_intent()
        self.put_book_in_basket()

        response = self.client.post(
            reverse("checkout"),
            self.checkout_data,
        )

        order = Order.objects.get()
        self.assertRedirects(
            response,
            reverse(
                "checkout_success",
                args=[order.order_number],
            ),
            fetch_redirect_response=False,
        )
        self.assertEqual(order.lineitems.get().book, self.book)
        self.assertEqual(order.grand_total, Decimal("11.00"))

        self.book.refresh_from_db()
        self.assertEqual(self.book.stock_quantity, 4)

    @patch("checkout.views.stripe.PaymentIntent.retrieve")
    def test_checkout_does_not_duplicate_an_existing_payment(
        self,
        retrieve_intent,
    ):
        retrieve_intent.return_value = self.successful_intent()
        self.put_book_in_basket()

        self.client.post(reverse("checkout"), self.checkout_data)
        self.client.post(reverse("checkout"), self.checkout_data)

        self.assertEqual(Order.objects.count(), 1)

        self.book.refresh_from_db()
        self.assertEqual(self.book.stock_quantity, 4)

    @patch("checkout.views.stripe.PaymentIntent.retrieve")
    def test_existing_webhook_order_redirects_after_stock_reaches_zero(
        self,
        retrieve_intent,
    ):
        retrieve_intent.return_value = self.successful_intent()
        self.book.stock_quantity = 1
        self.book.save(update_fields=["stock_quantity"])
        self.put_book_in_basket()

        self.client.post(reverse("checkout"), self.checkout_data)
        response = self.client.post(
            reverse("checkout"),
            self.checkout_data,
        )
        order = Order.objects.get()

        self.assertRedirects(
            response,
            reverse(
                "checkout_success",
                args=[order.order_number],
            ),
            fetch_redirect_response=False,
        )
        self.assertEqual(Order.objects.count(), 1)

    @patch("checkout.views.stripe.PaymentIntent.retrieve")
    def test_checkout_rejects_incorrect_payment_amount(
        self,
        retrieve_intent,
    ):
        retrieve_intent.return_value = SimpleNamespace(
            status="succeeded",
            amount=100,
            currency="gbp",
            client_secret="pi_test_order_secret_example",
        )
        self.put_book_in_basket()

        response = self.client.post(
            reverse("checkout"),
            self.checkout_data,
        )

        self.assertRedirects(
            response,
            reverse("checkout"),
            fetch_redirect_response=False,
        )
        self.assertFalse(Order.objects.exists())

    @patch("checkout.views.stripe.PaymentIntent.retrieve")
    def test_success_page_clears_basket(self, retrieve_intent):
        retrieve_intent.return_value = self.successful_intent()
        self.put_book_in_basket()
        self.client.post(reverse("checkout"), self.checkout_data)
        order = Order.objects.get()

        response = self.client.get(
            reverse(
                "checkout_success",
                args=[order.order_number],
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertNotIn("bag", self.client.session)
        self.assertContains(response, "Salt &amp; Hawthorn")
