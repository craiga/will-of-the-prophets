"""Test calculate_position."""

import pytest

from will_of_the_prophets import board
from factories import ButtholeFactory


@pytest.fixture(autouse=True)
def clear_caches():
    board.clear_caches()


@pytest.mark.django_db
def test_zero_rolls():
    assert board.calculate_position() == 1


@pytest.mark.django_db
def test_one_roll():
    assert board.calculate_position(22) == 23


@pytest.mark.django_db
def test_many_rolls():
    assert board.calculate_position(3, 20, 2, 40, 17, 5) == 88


@pytest.mark.django_db
def test_butthole():
    ButtholeFactory(start_square=88, end_square=5)
    assert board.calculate_position(3, 20, 2, 40, 17, 5, 2) == 7
