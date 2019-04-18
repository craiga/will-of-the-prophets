"""Butthole tests."""

from django.core.exceptions import ValidationError

import pytest
from model_mommy import mommy


@pytest.mark.django_db
def test_start_and_end_must_be_different():
    butthole = mommy.prepare("Butthole", start_square=25, end_square=25)
    with pytest.raises(ValidationError):
        butthole.full_clean()
