from django.conf import settings
from django.db import models


class AuthorProfile(models.Model):
    """
    Represents an author whose books can be listed on The Nook.

    An author may optionally be linked to a registered user account.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='author_profile'
    )

    display_name = models.CharField(
        max_length=150
    )

    bio = models.TextField(
        blank=True
    )

    website = models.URLField(
        blank=True
    )

    profile_image = models.ImageField(
        upload_to='authors/',
        null=True,
        blank=True
    )

    is_approved = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['display_name']

    def __str__(self):
        return self.display_name
