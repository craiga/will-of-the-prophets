"""Fixtures used across tests."""

from datetime import datetime

import pytest
import pytz
from model_bakery import baker


@pytest.fixture
def rolls():
    """Generate nine rolls on the first nine days of July 2369."""
    for number in range(1, 10):
        embargo = pytz.utc.localize(
            datetime(year=2369, month=7, day=number, hour=12, minute=34, second=56)
        )
        baker.make("Roll", number=number, embargo=embargo)
