"""Square tests."""

# pylint: disable=redefined-outer-name

from datetime import datetime

import pytest
import pytz
from model_mommy import mommy

from will_of_the_prophets import board


@pytest.fixture(autouse=True)
def clear_caches():
    board.clear_caches()


@pytest.fixture
def some_datetime():
    return pytz.utc.localize(
        datetime(year=2369, month=7, day=5, hour=12, minute=34, second=56)
    )


@pytest.mark.django_db
def test_get_special(some_datetime):
    """Test retrieving a square's special square type."""
    special = mommy.make("SpecialSquareType", image="")
    mommy.make("SpecialSquare", square=5, type=special)
    square = board.Square(number=5, current_position=1, now=some_datetime)
    assert special == square.get_special()


@pytest.mark.django_db
def test_not_special(some_datetime):
    square = board.Square(number=95, current_position=1, now=some_datetime)
    assert square.get_special() is None


@pytest.mark.django_db
def test_is_butthole_start(some_datetime):
    mommy.make("Butthole", start_square=50)
    square = board.Square(number=50, current_position=1, now=some_datetime)
    assert square.is_butthole_start() is True


@pytest.mark.django_db
def test_not_butthole_start(some_datetime):
    square = board.Square(number=17, current_position=1, now=some_datetime)
    assert square.is_butthole_start() is False


@pytest.mark.django_db
def test_get_butthole_ends(some_datetime):
    """Test getting the list of buttholes which end in this square."""
    for start_square in (55, 66, 77):
        mommy.make("Butthole", start_square=start_square, end_square=26)

    square = board.Square(number=26, current_position=1, now=some_datetime)
    assert set(square.get_butthole_ends()) == set([55, 66, 77])


@pytest.mark.django_db
def test_no_butthole_ends(some_datetime):
    square = board.Square(number=74, current_position=1, now=some_datetime)
    assert list(square.get_butthole_ends()) == []


@pytest.mark.django_db
@pytest.mark.parametrize(
    "number, pos, was_visited", [(74, 75, True), (75, 75, False), (76, 75, False)]
)
def test_was_visited(some_datetime, number, pos, was_visited):
    """Test that the was_visited flag is set correctly on squares."""
    square = board.Square(number=number, current_position=pos, now=some_datetime)
    assert square.was_visited == was_visited


@pytest.mark.django_db
@pytest.mark.parametrize(
    "number, pos, is_current_position",
    [(74, 75, False), (75, 75, True), (76, 75, False)],
)
def test_is_current_position(some_datetime, number, pos, is_current_position):
    """Test the is_current_position flag is set correctly."""
    square = board.Square(number=number, current_position=pos, now=some_datetime)
    assert square.is_current_position == is_current_position
