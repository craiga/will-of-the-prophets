"""Will of the Prophets game board."""

from django.template.loader import render_to_string
from django.utils import timezone

from will_of_the_prophets import models


def calculate_position(now):  # noqa: ANN001, ANN201
    """Calculate the position at a particular time."""
    position = 1
    for roll in models.Roll.objects.filter(embargo__lte=now):
        buttholes = {
            b.start_square: b.end_square
            for b in models.Butthole.objects.active(roll.embargo)
        }
        special_squares = {
            s.square: s.type
            for s in models.SpecialSquare.objects.select_related("type").active(
                roll.embargo
            )
        }

        position += roll.number

        # Handle position > 100.
        position = (position - 1) % 100 + 1

        if position in special_squares:
            position = position + special_squares[position].auto_move

        position = buttholes.get(position, position)

    return position


class Square:
    """A square in the board."""

    def __init__(  # noqa: D107, PLR0913
        self,
        number,  # noqa: ANN001
        current_position,  # noqa: ANN001
        now,  # noqa: ANN001
        row_reversed=False,  # noqa: ANN001, FBT002
        butthole_destination=None,  # noqa: ANN001
        butthole_source=None,  # noqa: ANN001
        special_square_type=None,  # noqa: ANN001
    ) -> None:
        self.now = now
        self.number = number
        self.row_reversed = row_reversed
        self.is_current_position = number == current_position
        self.was_visited = number < current_position
        self.butthole_destination = butthole_destination
        self.butthole_source = butthole_source
        self.special_square_type = special_square_type

    @property
    def row_break_after(self):  # noqa: ANN201, D102
        return str(self.number)[-1] == "1"


def square_numbers():  # noqa: ANN201
    """
    Square numbers in order, and whether the row is reversed.

    Starting from the bottom of the board, the first row of squares runs
    left-to-right, the second row runs right-to-left (that is, reversed),
    the third row runs left-to-right, and so on.
    """
    for row_number in reversed(range(10)):
        first_square = row_number * 10 + 1
        numbers = range(first_square, first_square + 10)
        row_reversed = False
        if row_number % 2:
            numbers = reversed(numbers)
            row_reversed = True

        for number in numbers:
            yield (number, row_reversed)


class Board:
    """The Will of the Riker - Quantum Leap board at any given time."""

    def __init__(self, now=None) -> None:  # noqa: ANN001, D107
        if not now:
            now = timezone.now()

        self.now = now
        buttholes = models.Butthole.objects.active(now)
        self.buttholes_start_to_end = {b.start_square: b.end_square for b in buttholes}
        self.buttholes_end_to_start = {b.end_square: b.start_square for b in buttholes}
        self.special_square_types = {
            s.square: s.type
            for s in models.SpecialSquare.objects.select_related("type").active(now)
        }

    @property
    def squares(self):  # noqa: ANN201
        """The 100 squares which make up the board."""
        current_position = self.get_current_position()
        for square_number, row_reversed in square_numbers():
            yield Square(
                number=square_number,
                now=self.now,
                current_position=current_position,
                row_reversed=row_reversed,
                butthole_destination=self.buttholes_start_to_end.get(square_number),
                butthole_source=self.buttholes_end_to_start.get(square_number),
                special_square_type=self.special_square_types.get(square_number),
            )

    def get_current_position(self):  # noqa: ANN201
        """Get the current position."""
        return calculate_position(self.now)

    def __str__(self) -> str:  # noqa: D105
        return render_to_string(
            "will_of_the_prophets/board/board.html", {"squares": self.squares}
        )
