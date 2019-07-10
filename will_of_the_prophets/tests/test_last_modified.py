"""Last-Modified response tests."""

# pylint: disable=unused-argument

import pytest


@pytest.mark.freeze_time("2369-07-05 08:00")
@pytest.mark.django_db
def test_last_modified_latest_roll(client, rolls):
    """Test that the Last-Modified date is the latest roll."""
    response = client.get("/", secure=True)
    assert response["Last-Modified"] == "Fri, 04 Jul 2369 12:34:56 GMT"


@pytest.mark.django_db
def test_last_modified_no_rolls(client):
    response = client.get("/", secure=True)
    assert "Last-Modified" not in response
