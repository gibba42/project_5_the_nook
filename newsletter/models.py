"""Models for newsletter subscriptions."""

from django.db import models


class NewsletterSubscriber(models.Model):
    """Store email addresses subscribed to The Nook newsletter."""

    email = models.EmailField(unique=True)
    subscribed_on = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        """Configure model display ordering."""

        ordering = ["-subscribed_on"]

    def __str__(self):
        """Return the subscriber email address."""

        return self.email
