"""Roll tests."""

# pylint: disable=redefined-outer-name

from datetime import timedelta

from django.core.exceptions import ValidationError
from django.utils import timezone

import pytest

from factories import RollFactory
from will_of_the_prophets.models import Roll


@pytest.fixture
def randint(mocker):
    return mocker.patch('random.randint', return_value=5)


@pytest.mark.django_db
def test_must_be_later_than_latest():
    """
    Test that a roll's embargo must be after other rolls' embargoes.

    This rule needs to be in place because the create new roll page
    assumes that the roll with the latest embargo date is the most recently
    created one.
    """
    RollFactory(embargo=timezone.now() + timedelta(days=5))
    roll = RollFactory.build(embargo=timezone.now() + timedelta(days=2))
    with pytest.raises(ValidationError):
        roll.full_clean()


def test_default_number(randint):
    roll = Roll()
    randint.assert_called_with(1, 6)
    assert roll.number == 5


def test_explicit_number(randint):
    roll = Roll(number=2)
    randint.assert_not_called()
    assert roll.number == 2
