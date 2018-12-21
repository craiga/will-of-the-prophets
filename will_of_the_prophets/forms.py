"""Will of the Prophets forms."""

from django import forms

from will_of_the_prophets import board, models


class RollForm(forms.ModelForm):
    """Roll form."""

    def save(self, commit=True):
        last_roll = models.Roll.objects.order_by("-embargo").first()
        if last_roll:
            game_board = board.Board(now=last_roll.embargo)
        else:
            game_board = board.Board()

        self.instance.number = board.roll_weighted_die(game_board)

        return super().save(commit=commit)

    class Meta:
        model = models.Roll
        fields = ["embargo"]
        labels = {"embargo": "Date and time the next move will be public"}
