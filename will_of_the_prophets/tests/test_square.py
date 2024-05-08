"""Square tests."""

import pytest

from will_of_the_prophets import board


@pytest.mark.django_db()
@pytest.mark.parametrize(
    ("number", "pos", "was_visited"), [(74, 75, True), (75, 75, False), (76, 75, False)]
)
def test_was_visited(some_datetime, number, pos, was_visited) -> None:  # noqa: ANN001
    """Test that the was_visited flag is set correctly on squares."""
    square = board.Square(number=number, current_position=pos, now=some_datetime)
    assert square.was_visited == was_visited


@pytest.mark.django_db()
@pytest.mark.parametrize(
    ("number", "pos", "is_current_position"),
    [(74, 75, False), (75, 75, True), (76, 75, False)],
)
def test_is_current_position(some_datetime, number, pos, is_current_position) -> None:  # noqa: ANN001
    """Test the is_current_position flag is set correctly."""
    square = board.Square(number=number, current_position=pos, now=some_datetime)
    assert square.is_current_position == is_current_position
