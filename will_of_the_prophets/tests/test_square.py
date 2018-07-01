"""Square tests."""

import pytest

from will_of_the_prophets import board
import factories


@pytest.fixture(autouse=True)
def clear_caches():
    board.clear_caches()


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
    factories.ButtholeFactory(start_square=50)
    square = board.Square(number=50)
    assert square.butthole_start is True


@pytest.mark.django_db
def test_not_butthole_start():
    square = board.Square(number=17)
    assert square.butthole_start is False


@pytest.mark.django_db
def test_butthole_ends():
    """Test getting the list of buttholes which end in this square."""
    for start_square in (55, 66, 77):
        factories.ButtholeFactory(start_square=start_square, end_square=26)

    square = board.Square(number=26)
    assert set(square.butthole_ends) == set([55, 66, 77])


@pytest.mark.django_db
def test_no_butthole_ends():
    square = board.Square(number=74)
    assert len(square.butthole_ends) == 0  # pylint: disable=len-as-condition
