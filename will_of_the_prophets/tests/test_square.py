"""Square tests."""

import pytest

from will_of_the_prophets import board
import factories


@pytest.mark.django_db
def test_special():
    """Test retrieving a square's special square type."""
    special = factories.SpecialSquareTypeFactory()
    factories.SpecialSquareFactory(square=5, type=special)
    square = board.Square(number=5)
    assert special == square.special


@pytest.mark.django_db
def test_not_special():
    square = board.Square(number=95)
    assert square.special is None


@pytest.mark.django_db
def test_butthole_start():
    butthole = factories.ButtholeFactory(start_square=50)
    square = board.Square(number=50)
    assert butthole == square.butthole_start


@pytest.mark.django_db
def test_not_butthole_start():
    square = board.Square(number=17)
    assert square.butthole_start is None


@pytest.mark.django_db
def test_butthole_end():
    """Test getting the list of buttholes which end in this square."""
    for start_square in (55, 66, 77):
        factories.ButtholeFactory(start_square=start_square, end_square=26)

    square = board.Square(number=26)
    assert len(square.butthole_end) == 3


@pytest.mark.django_db
def test_no_butthole_end():
    square = board.Square(number=74)
    assert len(square.butthole_end) == 0  # pylint: disable=len-as-condition
