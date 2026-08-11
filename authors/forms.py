from django import forms

from .models import AuthorProfile


class AuthorProfileForm(forms.ModelForm):
    """
    Form for creating and editing an author profile.
    """

    class Meta:
        model = AuthorProfile

        fields = (
            'display_name',
            'bio',
            'website',
            'profile_image',
        )

        labels = {
            'display_name': 'Author or pen name',
            'bio': 'Author biography',
            'website': 'Website or social media link',
            'profile_image': 'Author image',
        }

        widgets = {
            'bio': forms.Textarea(
                attrs={
                    'rows': 6,
                    'placeholder': (
                        'Tell readers a little about yourself.'
                    ),
                }
            ),
            'website': forms.URLInput(
                attrs={
                    'placeholder': 'https://example.com',
                }
            ),
            'profile_image': forms.FileInput(),
        }