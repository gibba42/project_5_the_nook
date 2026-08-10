"""Views for The Nook home application."""

from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse


def index(request):
    """Return the home page."""

    return render(request, "home/index.html")


def robots_txt(request):
    """Return crawling instructions for search engine robots."""

    sitemap_url = request.build_absolute_uri(
        reverse("django.contrib.sitemaps.views.sitemap")
    )

    lines = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /admin/",
        "Disallow: /accounts/",
        "Disallow: /bag/",
        "Disallow: /checkout/",
        "Disallow: /profile/",
        "Disallow: /authors/dashboard/",
        "Disallow: /authors/profile/",
        "Disallow: /books/manage/",
        "Disallow: /newsletter/",
        f"Sitemap: {sitemap_url}",
    ]

    return HttpResponse(
        "\n".join(lines),
        content_type="text/plain",
    )