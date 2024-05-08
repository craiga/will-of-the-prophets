"""Canonical link response tests."""

import pytest


@pytest.mark.django_db()
def test_canonical_link_header(client, settings) -> None:  # noqa: ANN001
    """Test that canonical link header is included when specified."""
    settings.PUBLIC_BOARD_CANONICAL_URL = "http://foo.bar/page"
    response = client.get("/", secure=True)
    assert response["Link"] == '<http://foo.bar/page>; rel="canonical"'


@pytest.mark.django_db()
def test_no_canonical_link_header(client, settings) -> None:  # noqa: ANN001
    """Test that canonical link header is not included when unspecified."""
    settings.PUBLIC_BOARD_CANONICAL_URL = None
    response = client.get("/", secure=True)
    assert "Link" not in response
