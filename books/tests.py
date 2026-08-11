from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db.models.deletion import ProtectedError
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from authors.models import AuthorProfile

from .models import Book, Genre


class BookModelTests(TestCase):
    """
    Tests for the Book model and its approval-related fields.
    """

    def setUp(self):
        """
        Create fresh test data before every test.
        """

        self.author = AuthorProfile.objects.create(
            display_name='Test Author',
            bio='An author created for automated testing.'
        )

        self.genre = Genre.objects.create(
            name='Fantasy',
            description='Fantasy books.'
        )

        self.reviewer = get_user_model().objects.create_user(
            username='staff_reviewer',
            email='reviewer@example.com',
            password='test-password-123'
        )

        self.book = Book.objects.create(
            author=self.author,
            genre=self.genre,
            title='The Test Book',
            isbn='9780000000001',
            description='A book created for automated testing.',
            price=Decimal('9.99'),
            stock_quantity=5
        )

    def test_book_string_returns_title(self):
        """
        The string representation should use the book title.
        """

        self.assertEqual(
            str(self.book),
            'The Test Book'
        )

    def test_new_book_defaults_to_draft(self):
        """
        New books should not be approved automatically.
        """

        self.assertEqual(
            self.book.status,
            Book.Status.DRAFT
        )

    def test_new_book_is_active_by_default(self):
        """
        New books should be operationally active by default.
        """

        self.assertTrue(self.book.is_active)

    def test_new_book_is_not_featured_by_default(self):
        """
        New books should not be featured automatically.
        """

        self.assertFalse(self.book.is_featured)

    def test_new_book_has_no_review_information(self):
        """
        A new book should not have approval or rejection information.
        """

        self.assertEqual(self.book.rejection_reason, '')
        self.assertIsNone(self.book.reviewed_by)
        self.assertIsNone(self.book.reviewed_at)

    def test_book_can_be_marked_as_pending(self):
        """
        A draft book can be moved to pending approval.
        """

        self.book.status = Book.Status.PENDING
        self.book.save()
        self.book.refresh_from_db()

        self.assertEqual(
            self.book.status,
            Book.Status.PENDING
        )

        self.assertEqual(
            self.book.get_status_display(),
            'Pending approval'
        )

    def test_book_can_store_approval_information(self):
        """
        An approved book can record who reviewed it and when.
        """

        reviewed_at = timezone.now()

        self.book.status = Book.Status.APPROVED
        self.book.reviewed_by = self.reviewer
        self.book.reviewed_at = reviewed_at
        self.book.save()
        self.book.refresh_from_db()

        self.assertEqual(
            self.book.status,
            Book.Status.APPROVED
        )

        self.assertEqual(
            self.book.reviewed_by,
            self.reviewer
        )

        self.assertEqual(
            self.book.reviewed_at,
            reviewed_at
        )

    def test_book_can_store_rejection_reason(self):
        """
        A rejected book can store feedback for the author.
        """

        self.book.status = Book.Status.REJECTED
        self.book.rejection_reason = (
            'Please provide a longer description.'
        )
        self.book.reviewed_by = self.reviewer
        self.book.reviewed_at = timezone.now()
        self.book.save()
        self.book.refresh_from_db()

        self.assertEqual(
            self.book.status,
            Book.Status.REJECTED
        )

        self.assertEqual(
            self.book.rejection_reason,
            'Please provide a longer description.'
        )

    def test_deleting_genre_does_not_delete_book(self):
        """
        Deleting a genre should set the book's genre to null.
        """

        self.genre.delete()
        self.book.refresh_from_db()

        self.assertIsNone(self.book.genre)

        self.assertTrue(
            Book.objects.filter(pk=self.book.pk).exists()
        )

    def test_deleting_author_with_books_is_prevented(self):
        """
        An author cannot be deleted while their books still exist.
        """

        with self.assertRaises(ProtectedError):
            self.author.delete()

        self.assertTrue(
            AuthorProfile.objects.filter(
                pk=self.author.pk
            ).exists()
        )

    def test_deleting_reviewer_keeps_book(self):
        """
        Deleting a staff reviewer should not delete reviewed books.
        """

        self.book.status = Book.Status.APPROVED
        self.book.reviewed_by = self.reviewer
        self.book.reviewed_at = timezone.now()
        self.book.save()

        self.reviewer.delete()
        self.book.refresh_from_db()

        self.assertIsNone(self.book.reviewed_by)

        self.assertTrue(
            Book.objects.filter(pk=self.book.pk).exists()
        )

        class BookSubmissionTests(TestCase):
            """
            Tests for the author book submission workflow.
            """

            def setUp(self):
                self.user = get_user_model().objects.create_user(
                    username='testauthor',
                    email='author@example.com',
                    password='test-password-123'
                )

                self.other_user = get_user_model().objects.create_user(
                    username='otherauthor',
                    email='other@example.com',
                    password='test-password-123'
                )

                self.author = AuthorProfile.objects.create(
                    user=self.user,
                    display_name='Test Author',
                    is_approved=True
                )

                self.other_author = AuthorProfile.objects.create(
                    user=self.other_user,
                    display_name='Other Author',
                    is_approved=True
                )

                self.genre = Genre.objects.create(
                    name='Science Fiction'
                )

                self.book = Book.objects.create(
                    author=self.author,
                    genre=self.genre,
                    title='Draft Book',
                    description='Test description.',
                    price=Decimal('9.99'),
                    stock_quantity=5
                )

            def test_author_can_submit_own_draft_book(self):
                self.client.login(
                    username='testauthor',
                    password='test-password-123'
                )

                response = self.client.post(
                    reverse(
                        'submit_book',
                        args=[self.book.id]
                    )
                )

                self.book.refresh_from_db()

                self.assertEqual(
                    self.book.status,
                    Book.Status.PENDING
                )

                self.assertRedirects(
                    response,
                    reverse('author_dashboard')
                )

            def test_author_cannot_edit_another_authors_book(self):
                self.client.login(
                    username='otherauthor',
                    password='test-password-123'
                )

                response = self.client.get(
                    reverse(
                        'edit_book',
                        args=[self.book.id]
                    )
                )

                self.assertEqual(
                    response.status_code,
                    404
                )

            def test_pending_book_cannot_be_edited(self):
                self.book.status = Book.Status.PENDING
                self.book.save()

                self.client.login(
                    username='testauthor',
                    password='test-password-123'
                )

                response = self.client.get(
                    reverse(
                        'edit_book',
                        args=[self.book.id]
                    )
                )

                self.assertRedirects(
                    response,
                    reverse('author_dashboard')
                )

            def test_author_cannot_delete_approved_book(self):
                self.book.status = Book.Status.APPROVED
                self.book.save()

                self.client.login(
                    username='testauthor',
                    password='test-password-123'
                )

                self.client.post(
                    reverse(
                        'delete_book',
                        args=[self.book.id]
                    )
                )

                self.assertTrue(
                    Book.objects.filter(
                        pk=self.book.pk
                    ).exists()
                )
