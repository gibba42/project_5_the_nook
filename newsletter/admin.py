"""Admin configuration for newsletter subscribers."""

from django.contrib import admin

from .models import NewsletterSubscriber


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    """Configure newsletter subscribers in Django admin."""

    list_display = (
        "email",
        "subscribed_on",
        "is_active",
    )

    list_filter = (
        "is_active",
        "subscribed_on",
    )

    search_fields = ("email",)

    readonly_fields = ("subscribed_on",)
