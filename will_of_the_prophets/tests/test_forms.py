"""Test forms."""

# pylint: disable=redefined-outer-name, unused-argument

from datetime import datetime

import pytest

from will_of_the_prophets import forms


@pytest.fixture
def roll_weighted_die(mocker):
    return mocker.patch(
        "will_of_the_prophets.board.roll_weighted_die", return_value=5
    )


@pytest.mark.django_db
def test_roll_form(roll_weighted_die):
    form = forms.RollForm({"embargo": datetime(1978, 3, 31, 12, 34)})
    roll = form.save(commit=False)
    assert roll.number == 5
