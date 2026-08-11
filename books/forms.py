from django import forms

from .models import Book


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