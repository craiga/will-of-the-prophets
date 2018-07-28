"""Will of the Prophets game board."""

from functools import lru_cache

from django.utils import timezone
from django.template.loader import render_to_string
from django.core import signals

from will_of_the_prophets import models


@lru_cache(maxsize=1)
def get_buttholes():
    """Get butthole starts and ends."""
    return dict(models.Butthole.objects.values_list('start_square',
                                                    'end_square'))


@lru_cache(maxsize=1)
def get_special_squares():
    """Get special square types keyed on squares they appear in."""
    squares = dict()
    for square in models.SpecialSquare.objects.select_related().all():
        squares[square.square] = square.type
    return squares


def clear_caches(**kwargs):  # pylint: disable=unused-argument
    """Clear cached results of buttholes and special squares."""
    get_buttholes.cache_clear()
    get_special_squares.cache_clear()


signals.request_started.connect(clear_caches)


def calculate_position(*rolls):
    """Calculate the current position."""
    buttholes = get_buttholes()
    position = 1
    for roll in rolls:
        position += roll
        if position in buttholes:
            position = buttholes[position]

    return (position - 1) % 100 + 1


class Square:
    """A square in the board."""

    def __init__(self, number, row_reversed=False, is_current_position=False):
        self.number = number
        self.row_reversed = row_reversed
        self.is_current_position = is_current_position

    @property
    def special(self):
        return get_special_squares().get(self.number)

    @property
    def butthole_start(self):
        return self.number in get_buttholes()

    @property
    def butthole_ends(self):
        """Get the starting squares of any buttholes which end here."""
        butthole_ends = []
        for start, end in get_buttholes().items():
            if end == self.number:
                butthole_ends.append(start)

        return butthole_ends

    @property
    def row_break_after(self):
        return str(self.number)[-1] == '1'


def square_numbers():
    """
    Square numbers in order, and whether the row is reversed.

    Starting from the bottom of the board, the first row of squares runs
    left-to-right, the second row runs right-to-left (i.e. reversed),
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
            yield Square(number=square_number, row_reversed=row_reversed,
                         is_current_position=is_current_position)

    def get_current_position(self):
        """Get the current position."""
        rolls = (models.Roll.objects
                 .filter(embargo__lte=self.now)
                 .order_by('embargo')
                 .values_list('number', flat=True))
        return calculate_position(*rolls)

    def __str__(self):
        return render_to_string('will_of_the_prophets/board/board.html',
                                {'squares': self.squares})
