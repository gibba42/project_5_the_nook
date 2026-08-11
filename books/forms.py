from django import forms

from .models import Book, Review


class BookForm(forms.ModelForm):
    """
    Form used by authors to create and edit their own books.
    """

    class Meta:
        model = Book

        fields = (
            'title',
            'genre',
            'isbn',
            'description',
            'price',
            'publication_date',
            'cover_image',
            'stock_quantity',
        )

        labels = {
            'title': 'Book title',
            'genre': 'Genre',
            'isbn': 'ISBN',
            'description': 'Book description',
            'price': 'Price',
            'publication_date': 'Publication date',
            'cover_image': 'Cover image',
            'stock_quantity': 'Stock quantity',
        }

        widgets = {
            'description': forms.Textarea(
                attrs={
                    'rows': 6,
                    'placeholder': (
                        'Tell readers what the book is about.'
                    ),
                }
            ),
            'publication_date': forms.DateInput(
                attrs={
                    'type': 'date',
                }
            ),
            'price': forms.NumberInput(
                attrs={
                    'step': '0.01',
                    'min': '0',
                }
            ),
            'stock_quantity': forms.NumberInput(
                attrs={
                    'min': '0',
                }
            ),
            'cover_image': forms.FileInput(),
        }


class ReviewForm(forms.ModelForm):
    """
    Form used by readers to create and edit book reviews.
    """

    class Meta:
        model = Review

        fields = (
            'rating',
            'title',
            'body',
        )

        labels = {
            'rating': 'Rating',
            'title': 'Review title',
            'body': 'Your review',
        }

        widgets = {
            'rating': forms.Select(
                choices=[
                    (5, '5 - Excellent'),
                    (4, '4 - Very good'),
                    (3, '3 - Good'),
                    (2, '2 - Fair'),
                    (1, '1 - Poor'),
                ]
            ),
            'title': forms.TextInput(
                attrs={
                    'placeholder': 'Optional short title',
                }
            ),
            'body': forms.Textarea(
                attrs={
                    'rows': 5,
                    'placeholder': (
                        'What did you think of the book?'
                    ),
                }
            ),
        }