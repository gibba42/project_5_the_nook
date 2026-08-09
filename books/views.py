from django.db.models import Avg, Q
from django.shortcuts import get_object_or_404, render

from .models import Book, Genre


def book_list(request):
    """
    Display all approved and active books in The Nook catalogue.

    Books can be searched, filtered by genre and sorted using
    query parameters supplied through the catalogue page.
    """

    books = (
        Book.objects
        .filter(
            is_active=True,
            status=Book.Status.APPROVED
        )
        .select_related('author', 'genre')
        .annotate(
            average_rating=Avg(
                'reviews__rating',
                filter=Q(reviews__is_approved=True)
            )
        )
    )

    genres = Genre.objects.all()

    search_term = request.GET.get('q', '').strip()
    selected_genres = request.GET.getlist('genre')
    sort = request.GET.get('sort', 'newest')

    if search_term:
        books = books.filter(
            Q(title__icontains=search_term)
            | Q(description__icontains=search_term)
            | Q(author__display_name__icontains=search_term)
        )

    if selected_genres:
        books = books.filter(
            genre__id__in=selected_genres
        )

    if sort == 'price_low':
        books = books.order_by('price')

    elif sort == 'price_high':
        books = books.order_by('-price')

    elif sort == 'title':
        books = books.order_by('title')

    elif sort == 'rating':
        books = books.order_by('-average_rating')

    else:
        books = books.order_by('-created_at')

    context = {
        'books': books,
        'genres': genres,
        'search_term': search_term,
        'selected_genres': selected_genres,
        'current_sort': sort,
    }

    return render(
        request,
        'books/book_list.html',
        context
    )


def book_detail(request, book_id):
    """
    Display the details for one approved and active book.
    """

    book = get_object_or_404(
        Book.objects
        .filter(
            is_active=True,
            status=Book.Status.APPROVED
        )
        .select_related('author', 'genre')
        .annotate(
            average_rating=Avg(
                'reviews__rating',
                filter=Q(reviews__is_approved=True)
            )
        ),
        pk=book_id
    )

    reviews = (
        book.reviews
        .filter(is_approved=True)
        .select_related('user')
    )

    context = {
        'book': book,
        'reviews': reviews,
    }

    return render(
        request,
        'books/book_detail.html',
        context
    )