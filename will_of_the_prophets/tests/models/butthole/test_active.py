from datetime import datetime  # noqa: D100

import pytest
from model_bakery import baker

from will_of_the_prophets import models


@pytest.mark.django_db
def test_no_start_or_end() -> None:  # noqa: D103
    butthole = baker.make(models.Butthole, start=None, end=None)
    assert butthole in models.Butthole.objects.active(datetime(2000, 1, 1))  # noqa: DTZ001


@pytest.mark.django_db
def test_start_in_past() -> None:  # noqa: D103
    butthole = baker.make(models.Butthole, start=datetime(1980, 1, 1), end=None)  # noqa: DTZ001
    assert butthole in models.Butthole.objects.active(datetime(2000, 1, 1))  # noqa: DTZ001


@pytest.mark.django_db
def test_start_in_future() -> None:  # noqa: D103
    butthole = baker.make(models.Butthole, start=datetime(2020, 1, 1), end=None)  # noqa: DTZ001
    assert butthole not in models.Butthole.objects.active(datetime(2000, 1, 1))  # noqa: DTZ001


@pytest.mark.django_db
def test_end_in_past() -> None:  # noqa: D103
    butthole = baker.make(models.Butthole, start=None, end=datetime(1980, 1, 1))  # noqa: DTZ001
    assert butthole not in models.Butthole.objects.active(datetime(2000, 1, 1))  # noqa: DTZ001


@pytest.mark.django_db
def test_end_in_future() -> None:  # noqa: D103
    butthole = baker.make(models.Butthole, start=None, end=datetime(2020, 1, 1))  # noqa: DTZ001
    assert butthole in models.Butthole.objects.active(datetime(2000, 1, 1))  # noqa: DTZ001


@pytest.mark.django_db
def test_start_and_end_in_past() -> None:  # noqa: D103
    butthole = baker.make(
        models.Butthole,
        start=datetime(1980, 1, 1),  # noqa: DTZ001
        end=datetime(1980, 2, 1),  # noqa: DTZ001
    )
    assert butthole not in models.Butthole.objects.active(datetime(2000, 1, 1))  # noqa: DTZ001


@pytest.mark.django_db
def test_start_in_past_end_in_future() -> None:  # noqa: D103
    butthole = baker.make(
        models.Butthole,
        start=datetime(1980, 1, 1),  # noqa: DTZ001
        end=datetime(2020, 1, 1),  # noqa: DTZ001
    )
    assert butthole in models.Butthole.objects.active(datetime(2000, 1, 1))  # noqa: DTZ001


@pytest.mark.django_db
def test_start_and_end_in_future() -> None:  # noqa: D103
    butthole = baker.make(
        models.Butthole,
        start=datetime(2020, 1, 1),  # noqa: DTZ001
        end=datetime(2020, 2, 1),  # noqa: DTZ001
    )
    assert butthole not in models.Butthole.objects.active(datetime(2000, 1, 1))  # noqa: DTZ001
