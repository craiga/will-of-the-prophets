"""Will of the Prophets forms."""

import random

from django import forms

from will_of_the_prophets.models import Roll


class RollForm(forms.ModelForm):
    """Roll form."""

    die_size = forms.ChoiceField(choices=[(100, "100-sided die"), (6, "Six-sided die")])

    def save(self, commit=True):
        """
        Save the roll with a random number between 1 and the selected die size.
        """
        obj = super().save(commit=False)
        obj.number = random.randint(1, int(self.cleaned_data["die_size"]))

        if commit:
            obj.save()

        return obj

    class Meta:
        model = Roll
        fields = ["embargo", "die_size"]
        labels = {"embargo": "Date and time move will be public"}
        widgets = {"embargo": forms.DateInput(attrs={"type": "date"})}
