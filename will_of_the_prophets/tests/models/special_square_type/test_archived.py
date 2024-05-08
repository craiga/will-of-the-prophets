from datetime import datetime  # noqa: D100

import pytest
from model_bakery import baker

from will_of_the_prophets import models


@pytest.mark.django_db()
def test_one_square_no_end() -> None:  # noqa: D103
    special_square_type = baker.make(models.SpecialSquareType, image="")
    baker.make(models.SpecialSquare, start=None, end=None, type=special_square_type)
    assert special_square_type not in models.SpecialSquareType.objects.archived(
        datetime(2000, 1, 1)  # noqa: DTZ001
    )


@pytest.mark.django_db()
def test_one_square_end_in_past() -> None:  # noqa: D103
    special_square_type = baker.make(models.SpecialSquareType, image="")
    baker.make(
        models.SpecialSquare,
        start=None,
        end=datetime(1980, 1, 1),  # noqa: DTZ001
        type=special_square_type,
    )
    assert special_square_type in models.SpecialSquareType.objects.archived(
        datetime(2000, 1, 1)  # noqa: DTZ001
    )


@pytest.mark.django_db()
def test_one_square_end_in_future() -> None:  # noqa: D103
    special_square_type = baker.make(models.SpecialSquareType, image="")
    baker.make(
        models.SpecialSquare,
        start=None,
        end=datetime(2020, 1, 1),  # noqa: DTZ001
        type=special_square_type,
    )
    assert special_square_type not in models.SpecialSquareType.objects.archived(
        datetime(2000, 1, 1)  # noqa: DTZ001
    )


@pytest.mark.django_db()
def test_many_squares_all_archived() -> None:  # noqa: D103
    special_square_type = baker.make(models.SpecialSquareType, image="")
    baker.make(
        models.SpecialSquare,
        start=None,
        end=datetime(1980, 1, 1),  # noqa: DTZ001
        type=special_square_type,
    )
    baker.make(
        models.SpecialSquare,
        start=datetime(1980, 1, 1),  # noqa: DTZ001
        end=datetime(1980, 2, 1),  # noqa: DTZ001
        type=special_square_type,
    )
    assert special_square_type in models.SpecialSquareType.objects.archived(
        datetime(2000, 1, 1)  # noqa: DTZ001
    )


@pytest.mark.django_db()
def test_many_squares_none_archived() -> None:  # noqa: D103
    special_square_type = baker.make(models.SpecialSquareType, image="")
    baker.make(models.SpecialSquare, start=None, end=None, type=special_square_type)
    baker.make(
        models.SpecialSquare,
        start=None,
        end=datetime(2020, 1, 1),  # noqa: DTZ001
        type=special_square_type,
    )

    assert special_square_type not in models.SpecialSquareType.objects.archived(
        datetime(2000, 1, 1)  # noqa: DTZ001
    )


@pytest.mark.django_db()
def test_many_squares_some_archived() -> None:  # noqa: D103
    special_square_type = baker.make(models.SpecialSquareType, image="")
    baker.make(models.SpecialSquare, start=None, end=None, type=special_square_type)
    baker.make(
        models.SpecialSquare,
        start=None,
        end=datetime(1980, 1, 1),  # noqa: DTZ001
        type=special_square_type,
    )
    baker.make(
        models.SpecialSquare,
        start=None,
        end=datetime(2020, 1, 1),  # noqa: DTZ001
        type=special_square_type,
    )
    assert special_square_type not in models.SpecialSquareType.objects.archived(
        datetime(2000, 1, 1)  # noqa: DTZ001
    )
