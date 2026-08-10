"""Tests for newsletter subscriptions."""

from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from .forms import NewsletterSignupForm
from .models import NewsletterSubscriber


class NewsletterSubscriberModelTests(TestCase):
    """Test the newsletter subscriber model."""

    def test_subscriber_can_be_created(self):
        """A newsletter subscriber can be stored."""

        subscriber = NewsletterSubscriber.objects.create(
            email="reader@example.com"
        )

        self.assertEqual(
            subscriber.email,
            "reader@example.com",
        )
        self.assertTrue(subscriber.is_active)

    def test_subscriber_string_returns_email(self):
        """The model string representation returns the email."""

        subscriber = NewsletterSubscriber.objects.create(
            email="reader@example.com"
        )

        self.assertEqual(
            str(subscriber),
            "reader@example.com",
        )


class NewsletterSignupFormTests(TestCase):
    """Test newsletter signup form validation."""

    def test_valid_email_is_accepted(self):
        """A valid unused email address passes validation."""

        form = NewsletterSignupForm(
            data={
                "email": "reader@example.com",
            }
        )

        self.assertTrue(form.is_valid())

    def test_invalid_email_is_rejected(self):
        """An invalid email address fails validation."""

        form = NewsletterSignupForm(
            data={
                "email": "not-an-email",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_duplicate_email_is_rejected(self):
        """An already subscribed email cannot subscribe again."""

        NewsletterSubscriber.objects.create(
            email="reader@example.com"
        )

        form = NewsletterSignupForm(
            data={
                "email": "reader@example.com",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_email_is_normalised_to_lowercase(self):
        """Submitted email addresses are stored in lowercase."""

        form = NewsletterSignupForm(
            data={
                "email": "Reader@Example.COM",
            }
        )

        self.assertTrue(form.is_valid())

        subscriber = form.save()

        self.assertEqual(
            subscriber.email,
            "reader@example.com",
        )


class NewsletterSignupViewTests(TestCase):
    """Test the newsletter signup view."""

    def setUp(self):
        """Store the signup URL used by the tests."""

        self.url = reverse("newsletter_signup")

    def test_valid_signup_creates_subscriber(self):
        """A valid POST creates a newsletter subscriber."""

        response = self.client.post(
            self.url,
            {
                "email": "reader@example.com",
            },
        )

        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            NewsletterSubscriber.objects.filter(
                email="reader@example.com"
            ).exists()
        )

    def test_valid_signup_displays_success_message(self):
        """Successful signup provides user feedback."""

        response = self.client.post(
            self.url,
            {
                "email": "reader@example.com",
            },
            follow=True,
        )

        messages = [
            str(message)
            for message in get_messages(response.wsgi_request)
        ]

        self.assertIn(
            "Thanks for subscribing to The Nook newsletter!",
            messages,
        )

    def test_duplicate_signup_does_not_create_second_record(self):
        """Duplicate email signup does not create another subscriber."""

        NewsletterSubscriber.objects.create(
            email="reader@example.com"
        )

        self.client.post(
            self.url,
            {
                "email": "reader@example.com",
            },
        )

        self.assertEqual(
            NewsletterSubscriber.objects.filter(
                email="reader@example.com"
            ).count(),
            1,
        )

    def test_duplicate_signup_displays_error_message(self):
        """Duplicate signup provides useful user feedback."""

        NewsletterSubscriber.objects.create(
            email="reader@example.com"
        )

        response = self.client.post(
            self.url,
            {
                "email": "reader@example.com",
            },
            follow=True,
        )

        messages = [
            str(message)
            for message in get_messages(response.wsgi_request)
        ]

        self.assertIn(
            (
                "This email address is already subscribed "
                "to The Nook newsletter."
            ),
            messages,
        )

    def test_signup_view_does_not_accept_get_requests(self):
        """Newsletter signup endpoint only accepts POST requests."""

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 405)