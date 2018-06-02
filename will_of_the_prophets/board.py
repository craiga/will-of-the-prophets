"""Will of the Prophets game board."""

from django.utils import timezone
from django.template.loader import render_to_string

from will_of_the_prophets import models


def calculate_position(*rolls):
    """Calculate the current position."""
    position = 1
    for roll in rolls:
        position += roll
        try:
            butthole = models.Butthole.objects.get(start_square=position)
            position = butthole.end_square
        except models.Butthole.DoesNotExist:
            pass

    return position


class Square:
    """A square in the board."""

    def __init__(self, number, is_current_position=False):
        self.number = number
        self.is_current_position = is_current_position

    @property
    def special(self):
        return (models.SpecialSquareType.objects
                .filter(squares__square=self.number)
                .first())

    @property
    def butthole_start(self):
        return models.Butthole.objects.filter(start_square=self.number).first()

    @property
    def butthole_end(self):
        return models.Butthole.objects.filter(end_square=self.number).all()

    @property
    def row_break_after(self):
        return str(self.number)[-1] == '1'


class Board:
    """The Will of the Prophets board at any given time."""

    def __init__(self, now=None):
        if not now:
            now = timezone.now()

        self.now = now

    @property
    def squares(self):
        """
        The 100 squares which make up the board.

        Order of squares is not sequential.
        """
        current_position = self.get_current_position()
        for row_number in reversed(range(0, 10)):
            if row_number % 2 == 0:
                for col_number in range(1, 11):
                    square_number = (row_number * 10) + col_number
                    is_current_position = square_number == current_position
                    yield Square(number=square_number,
                                 is_current_position=is_current_position)
            else:
                for col_number in reversed(range(1, 11)):
                    square_number = (row_number * 10) + col_number
                    is_current_position = square_number == current_position
                    yield Square(number=square_number,
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
