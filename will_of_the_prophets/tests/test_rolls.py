"""Roll tests."""

# pylint: disable=redefined-outer-name

from datetime import timedelta

from django.core.exceptions import ValidationError
from django.utils import timezone

import pytest
from model_bakery import baker


@pytest.mark.django_db
def test_must_be_later_than_latest():
    """
    Test that a roll's embargo must be after other rolls' embargoes.

    This rule needs to be in place because the create new roll page
    assumes that the roll with the latest embargo date is the most recently
    created one.
    """
    baker.make("Roll", embargo=timezone.now() + timedelta(days=5))
    roll = baker.prepare("Roll", embargo=timezone.now() + timedelta(days=2))
    with pytest.raises(ValidationError):
        roll.full_clean()
