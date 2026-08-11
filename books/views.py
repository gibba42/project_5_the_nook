from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Avg, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from .models import Book, Genre, Review
from .forms import BookForm, ReviewForm
from authors.models import AuthorProfile


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
    show_filters = request.GET.get('show_filters') == '1'

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
        'show_filters': show_filters,
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

    user_review = None

    if request.user.is_authenticated:
        user_review = Review.objects.filter(
            book=book,
            user=request.user
        ).first()

    context = {
        'book': book,
        'reviews': reviews,
        'user_review': user_review,
    }

    return render(
        request,
        'books/book_detail.html',
        context
    )


@staff_member_required
def approval_dashboard(request):
    """
    Display books awaiting staff approval.
    """

    pending_books = (
        Book.objects
        .filter(status=Book.Status.PENDING)
        .select_related('author', 'genre')
        .order_by('created_at')
    )

    context = {
        'pending_books': pending_books,
    }

    return render(
        request,
        'books/approval_dashboard.html',
        context
    )


@staff_member_required
def approval_detail(request, book_id):
    """
    Display a pending book for staff review.
    """

    book = get_object_or_404(
        Book.objects.select_related('author', 'genre'),
        pk=book_id,
        status=Book.Status.PENDING
    )

    context = {
        'book': book,
    }

    return render(
        request,
        'books/approval_detail.html',
        context
    )


@require_POST
@staff_member_required
def approve_book(request, book_id):
    """
    Approve a pending book and make it eligible for public display.
    """

    book = get_object_or_404(
        Book,
        pk=book_id,
        status=Book.Status.PENDING
    )

    book.status = Book.Status.APPROVED
    book.rejection_reason = ''
    book.reviewed_by = request.user
    book.reviewed_at = timezone.now()
    book.save()

    messages.success(
        request,
        f'"{book.title}" has been approved.'
    )

    return redirect('approval_dashboard')


@require_POST
@staff_member_required
def reject_book(request, book_id):
    """
    Reject a pending book and store the optional rejection reason.
    """

    book = get_object_or_404(
        Book,
        pk=book_id,
        status=Book.Status.PENDING
    )

    book.status = Book.Status.REJECTED
    book.rejection_reason = request.POST.get(
        'rejection_reason',
        ''
    ).strip()
    book.reviewed_by = request.user
    book.reviewed_at = timezone.now()
    book.save()

    messages.success(
        request,
        f'"{book.title}" has been rejected.'
    )

    return redirect('approval_dashboard')


@login_required
def create_book(request):
    """
    Allow an author to create a new draft book.
    """

    try:
        author_profile = request.user.author_profile
    except AuthorProfile.DoesNotExist:
        messages.error(
            request,
            'You need an author profile before you can add a book.'
        )
        return redirect('author_dashboard')

    if request.method == 'POST':
        form = BookForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():
            book = form.save(commit=False)

            book.author = author_profile
            book.status = Book.Status.DRAFT
            book.rejection_reason = ''
            book.reviewed_by = None
            book.reviewed_at = None

            book.save()

            messages.success(
                request,
                f'"{book.title}" has been saved as a draft.'
            )

            return redirect('author_dashboard')

        messages.error(
            request,
            'Please correct the errors in the form.'
        )

    else:
        form = BookForm()

    context = {
        'form': form,
        'page_title': 'Add a book',
        'button_text': 'Save draft',
    }

    return render(
        request,
        'books/book_form.html',
        context
    )


@login_required
def edit_book(request, book_id):
    """
    Allow an author to edit one of their own books.
    """

    book = get_object_or_404(
        Book,
        pk=book_id,
        author__user=request.user
    )

    if book.status == Book.Status.PENDING:
        messages.warning(
            request,
            'Books awaiting approval cannot be edited.'
        )
        return redirect('author_dashboard')

    if request.method == 'POST':
        form = BookForm(
            request.POST,
            request.FILES,
            instance=book
        )

        if form.is_valid():
            edited_book = form.save(commit=False)

            # Any rejected book becomes a draft again once edited.
            if edited_book.status == Book.Status.REJECTED:
                edited_book.status = Book.Status.DRAFT

            edited_book.rejection_reason = ''
            edited_book.reviewed_by = None
            edited_book.reviewed_at = None

            edited_book.save()

            messages.success(
                request,
                f'"{edited_book.title}" has been updated.'
            )

            return redirect('author_dashboard')

        messages.error(
            request,
            'Please correct the errors in the form.'
        )

    else:
        form = BookForm(instance=book)

    context = {
        'form': form,
        'book': book,
        'page_title': 'Edit book',
        'button_text': 'Save changes',
    }

    return render(
        request,
        'books/book_form.html',
        context
    )


@login_required
@require_POST
def delete_book(request, book_id):
    """
    Allow an author to delete one of their own draft or rejected books.
    """

    book = get_object_or_404(
        Book,
        pk=book_id,
        author__user=request.user
    )

    if book.status not in (
        Book.Status.DRAFT,
        Book.Status.REJECTED,
    ):
        messages.error(
            request,
            'Only draft or rejected books can be deleted.'
        )
        return redirect('author_dashboard')

    title = book.title

    if book.cover_image:
        book.cover_image.delete(save=False)

    book.delete()

    messages.success(
        request,
        f'"{title}" has been deleted.'
    )

    return redirect('author_dashboard')


@login_required
@require_POST
def submit_book(request, book_id):
    """
    Submit an author's draft or rejected book for staff approval.
    """

    book = get_object_or_404(
        Book,
        pk=book_id,
        author__user=request.user
    )

    if book.status not in (
        Book.Status.DRAFT,
        Book.Status.REJECTED,
    ):
        messages.error(
            request,
            'This book cannot currently be submitted.'
        )
        return redirect('author_dashboard')

    book.status = Book.Status.PENDING
    book.rejection_reason = ''
    book.reviewed_by = None
    book.reviewed_at = None

    book.save(
        update_fields=[
            'status',
            'rejection_reason',
            'reviewed_by',
            'reviewed_at',
            'updated_at',
        ]
    )

    messages.success(
        request,
        f'"{book.title}" has been submitted for approval.'
    )

    return redirect('author_dashboard')


@login_required
@require_POST
def remove_book_from_shop(request, book_id):
    """
    Allow an author to remove their approved book from the public shop
    without deleting its historical record.
    """

    book = get_object_or_404(
        Book,
        pk=book_id,
        author__user=request.user
    )

    if book.status != Book.Status.APPROVED:
        messages.error(
            request,
            'Only approved books can be removed from the shop.'
        )
        return redirect('author_dashboard')

    book.is_active = False
    book.save(update_fields=['is_active', 'updated_at'])

    messages.success(
        request,
        f'"{book.title}" has been removed from the shop.'
    )

    return redirect('author_dashboard')


@login_required
def add_review(request, book_id):
    """
    Allow a logged-in reader to review an approved book.
    """

    book = get_object_or_404(
        Book,
        pk=book_id,
        status=Book.Status.APPROVED,
        is_active=True
    )

    existing_review = Review.objects.filter(
        book=book,
        user=request.user
    ).first()

    if existing_review:
        messages.info(
            request,
            'You have already reviewed this book.'
        )
        return redirect(
            'edit_review',
            review_id=existing_review.id
        )

    if request.method == 'POST':
        form = ReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)

            review.book = book
            review.user = request.user

            review.save()

            messages.success(
                request,
                'Thank you. Your review has been added.'
            )

            return redirect(
                'book_detail',
                book_id=book.id
            )

    else:
        form = ReviewForm()

    context = {
        'form': form,
        'book': book,
        'page_title': 'Review this book',
        'button_text': 'Post review',
    }

    return render(
        request,
        'books/review_form.html',
        context
    )


@login_required
def edit_review(request, review_id):
    """
    Allow a reader to edit their own review.
    """

    review = get_object_or_404(
        Review,
        pk=review_id,
        user=request.user
    )

    if request.method == 'POST':
        form = ReviewForm(
            request.POST,
            instance=review
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                'Your review has been updated.'
            )

            return redirect(
                'book_detail',
                book_id=review.book.id
            )

    else:
        form = ReviewForm(instance=review)

    context = {
        'form': form,
        'book': review.book,
        'review': review,
        'page_title': 'Edit your review',
        'button_text': 'Save review',
    }

    return render(
        request,
        'books/review_form.html',
        context
    )


@login_required
@require_POST
def delete_review(request, review_id):
    """
    Allow a reader to delete their own review.
    """

    review = get_object_or_404(
        Review,
        pk=review_id,
        user=request.user
    )

    book_id = review.book.id

    review.delete()

    messages.success(
        request,
        'Your review has been deleted.'
    )

    return redirect(
        'book_detail',
        book_id=book_id
    )
