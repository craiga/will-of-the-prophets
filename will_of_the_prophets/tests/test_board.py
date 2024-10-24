"""Board tests."""

from datetime import datetime

from django.core.management import call_command

import pytest
import pytz

from will_of_the_prophets import board


@pytest.mark.django_db
def test_square_order() -> None:
    """
    Tests that squares are generated as expected.

    Squares aren't in numeric order—the order needs to match the order they're
    displayed on the board.

    The ordering is as follows:

       100 99 … 92 91   (reversed)
        81 82 … 89 90
        80 79 … 72 71   (reversed)
        …
        21 22 … 29 30
        20 19 … 12 11   (reversed)
        01 02 … 09 10
    """
    the_board = board.Board()
    squares = list(the_board.squares)
    assert len(squares) == 100
    for i, expected_number, expected_row_reversed in (
        (0, 100, True),
        (1, 99, True),
        (9, 91, True),
        (10, 81, False),
        (11, 82, False),
        (19, 90, False),
        (20, 80, True),
        (80, 20, True),
        (89, 11, True),
        (90, 1, False),
        (99, 10, False),
    ):
        assert squares[i].number == expected_number
        assert squares[i].row_reversed == expected_row_reversed


@pytest.mark.django_db
@pytest.mark.freeze_time("2369-07-05 08:00")
def test_position(rolls) -> None:  # noqa: ANN001
    """Test that the current position is correctly set."""
    the_board = board.Board()
    assert the_board.get_current_position() == 11

    squares = list(the_board.squares)
    assert squares[89].number == 11
    assert squares[89].is_current_position
    for i in range(99):
        if i == 89:
            continue

        assert not squares[i].is_current_position


@pytest.mark.django_db
@pytest.mark.freeze_time("2369-07-05 08:00")
def test_explicit_date(rolls) -> None:  # noqa: ANN001
    """Test that the current position is set with an explicit date."""
    the_board = board.Board(
        now=datetime(year=2369, month=7, day=8, hour=20, tzinfo=pytz.utc)
    )
    assert the_board.get_current_position() == 37

    squares = list(the_board.squares)
    assert squares[63].number == 37
    assert squares[63].is_current_position
    for i in range(99):
        if i == 63:
            continue

        assert not squares[i].is_current_position


@pytest.mark.django_db
def test_query_count(django_assert_max_num_queries) -> None:  # noqa: ANN001
    """Test that rendering the board does not issue an excessive number of queries."""
    call_command(
        "loaddata", "buttholes", "special-square-types", "special-squares", "rolls"
    )
    with django_assert_max_num_queries(600):
        str(board.Board())


@pytest.fixture
def some_datetime():  # noqa: ANN201, D103
    return pytz.utc.localize(
        datetime(year=2369, month=7, day=5, hour=12, minute=34, second=56)  # noqa: DTZ001
    )
