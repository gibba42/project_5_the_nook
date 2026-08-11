from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from authors.models import AuthorProfile
from books.models import Book


class BasketViewTests(TestCase):
    def setUp(self):
        author = AuthorProfile.objects.create(display_name="Rowan Vale")
        self.book = Book.objects.create(
            author=author,
            title="The Mapmaker's Lantern",
            description="A test book.",
            price=Decimal("12.99"),
            stock_quantity=3,
            status=Book.Status.APPROVED,
        )

    def test_add_book_to_basket(self):
        response = self.client.post(
            reverse("add_to_bag", args=[self.book.pk]),
            {"quantity": "2", "redirect_url": reverse("view_bag")},
        )

        self.assertRedirects(response, reverse("view_bag"))
        self.assertEqual(
            self.client.session["bag"],
            {str(self.book.pk): 2},
        )

    def test_add_rejects_quantity_above_stock(self):
        self.client.post(
            reverse("add_to_bag", args=[self.book.pk]),
            {"quantity": "2"},
        )
        self.client.post(
            reverse("add_to_bag", args=[self.book.pk]),
            {"quantity": "2"},
        )

        self.assertEqual(self.client.session["bag"][str(self.book.pk)], 2)

    def test_unapproved_book_cannot_be_added(self):
        self.book.status = Book.Status.PENDING
        self.book.save(update_fields=["status"])

        response = self.client.post(
            reverse("add_to_bag", args=[self.book.pk]),
            {"quantity": "1"},
        )

        self.assertEqual(response.status_code, 404)
        self.assertNotIn("bag", self.client.session)

    def test_adjust_book_quantity(self):
        session = self.client.session
        session["bag"] = {str(self.book.pk): 1}
        session.save()

        response = self.client.post(
            reverse("adjust_bag", args=[self.book.pk]),
            {"quantity": "3"},
        )

        self.assertRedirects(response, reverse("view_bag"))
        self.assertEqual(self.client.session["bag"][str(self.book.pk)], 3)

    def test_remove_book_from_basket(self):
        session = self.client.session
        session["bag"] = {str(self.book.pk): 1}
        session.save()

        response = self.client.post(
            reverse("remove_from_bag", args=[self.book.pk]),
        )

        self.assertRedirects(response, reverse("view_bag"))
        self.assertEqual(self.client.session["bag"], {})

    def test_basket_page_displays_book_and_totals(self):
        session = self.client.session
        session["bag"] = {str(self.book.pk): 2}
        session.save()

        response = self.client.get(reverse("view_bag"))

        self.assertContains(response, "The Mapmaker&#x27;s Lantern")
        self.assertContains(response, "£25.98")
        self.assertContains(response, "£28.58")

    def test_basket_changes_require_post(self):
        response = self.client.get(
            reverse("add_to_bag", args=[self.book.pk])
        )
        self.assertEqual(response.status_code, 405)
