"""Pytest fixtures used across tests."""

from datetime import datetime

import pytest
import pytz
from model_mommy import mommy


@pytest.fixture
def rolls():
    """Generate nine rolls on the first nine days of July 2369."""
    for number in range(1, 10):
        embargo = datetime(
            year=2369,
            month=7,
            day=number,
            hour=12,
            minute=34,
            second=56,
            tzinfo=pytz.utc,
        )
        mommy.make("Roll", number=number, embargo=embargo)
