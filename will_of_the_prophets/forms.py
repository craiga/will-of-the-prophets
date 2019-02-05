"""Will of the Prophets forms."""

from django import forms

from will_of_the_prophets.models import Roll


class RollForm(forms.ModelForm):
    """Roll form."""

    class Meta:
        model = Roll
        fields = ["embargo"]
        labels = {"embargo": "Date and time the next move will be public"}
