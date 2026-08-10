"""Sitemap configuration for The Nook."""

from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from books.models import Book


class StaticViewSitemap(Sitemap):
    """Sitemap entries for important public static pages."""

    changefreq = "weekly"

    def items(self):
        """Return the named public views included in the sitemap."""

        return [
            "home",
            "book_list",
        ]

    def location(self, item):
        """Return the URL for a named public view."""

        return reverse(item)

    def priority(self, item):
        """Set relative priorities for key public pages."""

        priorities = {
            "home": 1.0,
            "book_list": 0.9,
        }

        return priorities.get(item, 0.5)


class BookSitemap(Sitemap):
    """Sitemap entries for public books."""

    changefreq = "weekly"
    priority = 0.7

    def items(self):
        """Return only approved and active books."""

        return Book.objects.filter(
            is_active=True,
            status=Book.Status.APPROVED,
        )

    def location(self, book):
        """Return the public detail URL for a book."""

        return reverse(
            "book_detail",
            args=[book.pk],
        )

    def lastmod(self, book):
        """Return the date the book was last updated."""

        return book.updated_at