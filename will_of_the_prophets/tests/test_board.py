"""Board tests."""

from datetime import datetime

import pytest
import pytz

from will_of_the_prophets import board
import factories


@pytest.fixture
def rolls():
    """Generate nine rolls on the first nine days of July 2369."""
    for number in range(1, 10):
        embargo = datetime(year=2369, month=7, day=number,
                           hour=12, minute=34, second=56, tzinfo=pytz.utc)
        factories.RollFactory(number=number, embargo=embargo)


@pytest.mark.django_db
def test_squares():
    """
    Tests that squares are generated as expected.
    
    Squares aren't in numeric order—the order needs to match the order they're
    displayed on the board.

    The ordering is as follows:

       100 99 … 92 91
        81 82 … 89 90
        80 79 … 72 71
        …
        21 22 … 29 30
        20 19 … 12 11
        01 02 … 09 10
    """
    the_board = board.Board()
    squares = list(the_board.squares)
    assert len(squares) == 100
    for i, expected_number in  ((0, 100), (1, 99), (8, 92), (9, 91),
                                (10, 81), (11, 82), (18, 89), (19, 90),
                                (20, 80), (21, 79), (28, 72), (29, 71),
                                (70, 21), (71, 22), (78, 29), (79, 30),
                                (80, 20), (81, 19), (88, 12), (89, 11),
                                (90, 1), (91, 2), (98, 9), (99, 10)):
        assert squares[i].number == expected_number


@pytest.mark.django_db
@pytest.mark.usefixtures('rolls')
@pytest.mark.freeze_time('2369-07-05 08:00')
def test_position():
    """Test that the current position is correctly set."""
    the_board = board.Board()
    assert the_board.get_current_position() == 11

    squares = list(the_board.squares)
    assert squares[89].number == 11
    assert squares[89].is_current_position
    for i in range(0, 99):
        if i == 89:
            continue

        assert not squares[i].is_current_position

@pytest.mark.django_db
@pytest.mark.usefixtures('rolls')
@pytest.mark.freeze_time('2369-07-05 08:00')
def test_explicit_date():
    """Test that the current position is set with an explicit date."""
    the_board = board.Board(now=datetime(year=2369, month=7, day=8, hour=20,
                                         tzinfo=pytz.utc))
    assert the_board.get_current_position() == 37

    squares = list(the_board.squares)
    assert squares[63].number == 37
    assert squares[63].is_current_position
    for i in range(0, 99):
        if i == 63:
            continue

        assert not squares[i].is_current_position
