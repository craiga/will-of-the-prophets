"""Butthole tests."""

from django.core.exceptions import ValidationError

import pytest

from factories import ButtholeFactory, SpecialSquareFactory


@pytest.fixture
def special_square_50():
    return SpecialSquareFactory(square=50)


@pytest.fixture
def butthole_75_to_25():
    return ButtholeFactory(start_square=75, end_square=25)


@pytest.mark.django_db
def test_start_and_end_must_be_different():
    butthole = ButtholeFactory.build(start_square=25, end_square=25)
    with pytest.raises(ValidationError):
        butthole.full_clean()


@pytest.mark.django_db
@pytest.mark.usefixtures('special_square_50')
def test_start_square_cannot_be_special():
    """Test that start square cannot be in special square."""
    butthole = ButtholeFactory.build(start_square=50, end_square=25)
    with pytest.raises(ValidationError):
        butthole.full_clean()


@pytest.mark.django_db
@pytest.mark.usefixtures('special_square_50')
def test_end_can_be_in_special_square():
    butthole = ButtholeFactory.build(start_square=75, end_square=50)
    butthole.full_clean()


@pytest.mark.django_db
@pytest.mark.usefixtures('butthole_75_to_25')
def test_start_squares_cannot_overlap():
    """Test that start squares cannot overlap."""
    butthole = ButtholeFactory.build(start_square=75, end_square=50)
    with pytest.raises(ValidationError):
        butthole.validate_unique()


@pytest.mark.django_db
@pytest.mark.usefixtures('butthole_75_to_25')
def test_end_squares_can_overlap():
    butthole = ButtholeFactory.build(start_square=50, end_square=25)
    butthole.full_clean()
