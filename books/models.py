from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from authors.models import AuthorProfile


class Genre(models.Model):
    """
    A genre used to categorise books in the store.
    """

    name = models.CharField(
        max_length=100,
        unique=True
    )

    description = models.TextField(
        blank=True
    )

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    A book available for purchase through The Nook.
    """

    author = models.ForeignKey(
        AuthorProfile,
        on_delete=models.PROTECT,
        related_name='books'
    )

    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='books'
    )

    title = models.CharField(
        max_length=255
    )

    isbn = models.CharField(
        max_length=20,
        unique=True,
        null=True,
        blank=True
    )

    description = models.TextField()

    price = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    publication_date = models.DateField(
        null=True,
        blank=True
    )

    cover_image = models.ImageField(
        upload_to='books/',
        null=True,
        blank=True
    )

    stock_quantity = models.PositiveIntegerField(
        default=0
    )

    is_featured = models.BooleanField(
        default=False
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class Review(models.Model):
    """
    A reader review for a book.

    A user can leave a maximum of one review per book.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='book_reviews'
    )

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    rating = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5),
        ]
    )

    title = models.CharField(
        max_length=150,
        blank=True
    )

    body = models.TextField()

    is_approved = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['-created_at']

        constraints = [
            models.UniqueConstraint(
                fields=['user', 'book'],
                name='unique_user_book_review'
            )
        ]

    def __str__(self):
        return f'{self.user} - {self.book} ({self.rating}/5)'