"""Special square tests."""

# pylint: disable=redefined-outer-name, unused-argument

from django.core.exceptions import ValidationError

import pytest

import factories


@pytest.fixture
def special_square_type():
    return factories.SpecialSquareTypeFactory()


@pytest.fixture
def butthole():
    return factories.ButtholeFactory(start_square=75, end_square=25)


@pytest.mark.django_db
def test_cannot_exist_at_butthole_start(special_square_type, butthole):
    """Assert a special square cannot exist at the start of a butthole."""
    square = factories.SpecialSquareFactory.build(square=75,
                                                  type=special_square_type)
    with pytest.raises(ValidationError):
        square.full_clean()


@pytest.mark.django_db
def test_can_exist_at_butthole_end(special_square_type, butthole):
    """Assert a special square can exist at the end of a butthole."""
    square = factories.SpecialSquareFactory.build(square=25,
                                                  type=special_square_type)
    square.full_clean()
