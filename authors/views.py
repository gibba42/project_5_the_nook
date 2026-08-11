from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AuthorProfileForm
from .models import AuthorProfile

def author_list(request):
    """
    Display approved authors with published books.
    """

    authors = (
        AuthorProfile.objects
        .filter(is_approved=True)
        .prefetch_related('books')
        .order_by('display_name')
    )

    context = {
        'authors': authors,
    }

    return render(
        request,
        'authors/author_list.html',
        context
    )

@login_required
def author_dashboard(request):
    """
    Display the logged-in user's author profile and book listings.
    """

    try:
        author_profile = request.user.author_profile

        books = (
            author_profile.books
            .select_related('genre')
            .order_by('-updated_at')
        )

    except AuthorProfile.DoesNotExist:
        author_profile = None
        books = []

    context = {
        'author_profile': author_profile,
        'books': books,
    }

    return render(
        request,
        'authors/author_dashboard.html',
        context
    )


@login_required
def create_author_profile(request):
    """
    Allow a logged-in user to create one author profile.
    """

    if AuthorProfile.objects.filter(user=request.user).exists():
        messages.info(
            request,
            'You already have an author profile.'
        )

        return redirect('author_dashboard')

    if request.method == 'POST':
        form = AuthorProfileForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():
            author_profile = form.save(commit=False)
            author_profile.user = request.user
            author_profile.save()

            messages.success(
                request,
                'Your author profile has been created.'
            )

            return redirect('author_dashboard')

        messages.error(
            request,
            'Please correct the errors in the form.'
        )

    else:
        form = AuthorProfileForm()

    context = {
        'form': form,
        'page_title': 'Create your author profile',
        'button_text': 'Create profile',
    }

    return render(
        request,
        'authors/author_profile_form.html',
        context
    )


@login_required
def edit_author_profile(request):
    """
    Allow users to edit only their own author profile.
    """

    author_profile = get_object_or_404(
        AuthorProfile,
        user=request.user
    )

    if request.method == 'POST':
        form = AuthorProfileForm(
            request.POST,
            request.FILES,
            instance=author_profile
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                'Your author profile has been updated.'
            )

            return redirect('author_dashboard')

        messages.error(
            request,
            'Please correct the errors in the form.'
        )

    else:
        form = AuthorProfileForm(
            instance=author_profile
        )

    context = {
        'form': form,
        'page_title': 'Edit your author profile',
        'button_text': 'Save changes',
    }

    return render(
        request,
        'authors/author_profile_form.html',
        context
    )