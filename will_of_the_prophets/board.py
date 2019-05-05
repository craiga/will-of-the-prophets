"""Will of the Prophets game board."""

from functools import lru_cache

from django.core import signals
from django.template.loader import render_to_string
from django.utils import timezone

from will_of_the_prophets import models


@lru_cache(maxsize=1)
def get_all_buttholes():
    """Get all buttholes."""
    return models.Butthole.objects.all()


@lru_cache(maxsize=1)
def get_all_special_squares():
    """Get all special squares."""
    return models.SpecialSquare.objects.select_related().all()


def clear_caches(**kwargs):  # pylint: disable=unused-argument
    """Clear cached results of buttholes and special squares."""
    get_all_buttholes.cache_clear()
    get_all_special_squares.cache_clear()


signals.request_started.connect(clear_caches)


def calculate_position(now):
    """Calculate the position at a particular time."""
    position = 1
    for roll in models.Roll.objects.filter(embargo__lte=now):
        buttholes = get_buttholes(roll.embargo)
        special_squares = get_special_squares(roll.embargo)

        position += roll.number

        if position in special_squares:
            position = position + special_squares[position].auto_move

        position = buttholes.get(position, position)

    return (position - 1) % 100 + 1


def is_active(obj, now):
    """Determine if an object is active."""
    if not obj.start or obj.start <= now:
        if not obj.end or obj.end >= now:
            return True

    return False


def get_buttholes(now):
    """Get butthole starts and ends."""
    buttholes = dict()
    for butthole in get_all_buttholes():
        if is_active(butthole, now):
            buttholes[butthole.start_square] = butthole.end_square

    return buttholes


def get_special_squares(now):
    """Get special square types keyed on squares they appear in."""
    special_squares = dict()
    for special_square in get_all_special_squares():
        if is_active(special_square, now):
            special_squares[special_square.square] = special_square.type

    return special_squares


class Square:
    """A square in the board."""

    def __init__(self, number, now, row_reversed=False, is_current_position=False, was_visited=False):
        self.now = now
        self.number = number
        self.row_reversed = row_reversed
        self.is_current_position = is_current_position
        self.was_visited = was_visited

    def get_special(self):
        return get_special_squares(self.now).get(self.number)

    def is_butthole_start(self):
        return self.number in get_buttholes(self.now)

    def get_butthole_ends(self):
        """Get the starting squares of any buttholes which end here."""
        butthole_ends = []
        for start, end in get_buttholes(self.now).items():
            if end == self.number:
                butthole_ends.append(start)

        return butthole_ends

    @property
    def row_break_after(self):
        return str(self.number)[-1] == "1"


def square_numbers():
    """
    Square numbers in order, and whether the row is reversed.

    Starting from the bottom of the board, the first row of squares runs
    left-to-right, the second row runs right-to-left (that is, reversed),
    the third row runs left-to-right, and so on.
    """
    for row_number in reversed(range(0, 10)):
        first_square = row_number * 10 + 1
        numbers = range(first_square, first_square + 10)
        row_reversed = False
        if row_number % 2:
            numbers = reversed(numbers)
            row_reversed = True

        for number in numbers:
            yield (number, row_reversed)


class Board:
    """The Will of the Prophets board at any given time."""

    def __init__(self, now=None):
        if not now:
            now = timezone.now()

        self.now = now

    @property
    def squares(self):
        """The 100 squares which make up the board."""
        current_position = self.get_current_position()
        for square_number, row_reversed in square_numbers():
            is_current_position = square_number == current_position
            was_visited = square_number < current_position
            yield Square(
                number=square_number,
                now=self.now,
                row_reversed=row_reversed,
                is_current_position=is_current_position,
                was_visited=was_visited,
            )

    def get_current_position(self):
        """Get the current position."""
        return calculate_position(self.now)

    def __str__(self):
        return render_to_string(
            "will_of_the_prophets/board/board.html", {"squares": self.squares}
        )
