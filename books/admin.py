from django.contrib import admin

from .models import Book, Genre, Review


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):

    list_display = (
        'name',
    )

    search_fields = (
        'name',
    )


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'author',
        'genre',
        'price',
        'status',
        'reviewed_by',
        'stock_quantity',
        'is_active',
        'is_featured',
    )

    list_filter = (
        'status',
        'is_active',
        'is_featured',
        'genre',
    )

    search_fields = (
        'title',
        'author__display_name',
        'isbn',
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):

    list_display = (
        'book',
        'user',
        'rating',
        'is_approved',
        'created_at',
    )

    list_filter = (
        'rating',
        'is_approved',
    )

    search_fields = (
        'book__title',
        'user__username',
        'body',
    )
