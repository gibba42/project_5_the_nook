from django import forms

from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    """Form for updating a reader's saved delivery information."""

    class Meta:
        model = UserProfile
        fields = (
            "default_phone_number",
            "default_street_address1",
            "default_street_address2",
            "default_town_or_city",
            "default_county",
            "default_postcode",
            "default_country",
        )
        labels = {
            "default_phone_number": "Phone number",
            "default_street_address1": "Address line 1",
            "default_street_address2": "Address line 2",
            "default_town_or_city": "Town or city",
            "default_county": "County",
            "default_postcode": "Postcode",
            "default_country": "Country",
        }
        widgets = {
            "default_phone_number": forms.TextInput(
                attrs={
                    "placeholder": "Phone number",
                    "autocomplete": "tel",
                }
            ),
            "default_street_address1": forms.TextInput(
                attrs={
                    "placeholder": "Address line 1",
                    "autocomplete": "address-line1",
                }
            ),
            "default_street_address2": forms.TextInput(
                attrs={
                    "placeholder": "Address line 2 (optional)",
                    "autocomplete": "address-line2",
                }
            ),
            "default_town_or_city": forms.TextInput(
                attrs={
                    "placeholder": "Town or city",
                    "autocomplete": "address-level2",
                }
            ),
            "default_county": forms.TextInput(
                attrs={
                    "placeholder": "County",
                    "autocomplete": "address-level1",
                }
            ),
            "default_postcode": forms.TextInput(
                attrs={
                    "placeholder": "Postcode",
                    "autocomplete": "postal-code",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            if field_name == "default_country":
                field.widget.attrs["class"] = "form-select"
            else:
                field.widget.attrs["class"] = "form-control"