"""Forms for newsletter subscriptions."""

from django import forms

from .models import NewsletterSubscriber


class NewsletterSignupForm(forms.ModelForm):
    """Allow visitors to subscribe to The Nook newsletter."""

    class Meta:
        """Configure the newsletter signup form."""

        model = NewsletterSubscriber
        fields = ["email"]

        widgets = {
            "email": forms.EmailInput(
                attrs={
                    "placeholder": "Your email address",
                    "autocomplete": "email",
                    "aria-label": "Email address",
                }
            ),
        }

    def clean_email(self):
        """Normalise and validate newsletter email addresses."""

        email = self.cleaned_data["email"].strip().lower()

        if NewsletterSubscriber.objects.filter(
            email__iexact=email,
            is_active=True,
        ).exists():
            raise forms.ValidationError(
                "This email address is already subscribed."
            )

        return email