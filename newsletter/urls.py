"""URL configuration for newsletter subscriptions."""

from django.urls import path

from . import views


urlpatterns = [
    path(
        "signup/",
        views.newsletter_signup,
        name="newsletter_signup",
    ),
]