"""Will of the Prophets forms."""

from django import forms

from will_of_the_prophets import board, models


class RollForm(forms.ModelForm):
    """Roll form."""

    def save(self, commit=False):
        self.instance.number = board.roll_weighted_dice()
        return super().save(commit=commit)

    class Meta:
        model = models.Roll
        fields = ["embargo"]
        labels = {"embargo": "Date and time the next move will be public"}
