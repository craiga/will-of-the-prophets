"""Canonical link response tests."""

# pylint: disable=unused-argument

import pytest


@pytest.mark.django_db
def test_canonical_link_header(client, settings):
    """Test that canonical link header is included when specified."""
    settings.PUBLIC_BOARD_CANONICAL_URL = "http://foo.bar/page"
    response = client.get("/")
    assert response["Link"] == '<http://foo.bar/page>; rel="canonical"'


@pytest.mark.django_db
def test_no_canonical_link_header(client, settings):
    """Test that canonical link header is not included when unspecified."""
    settings.PUBLIC_BOARD_CANONICAL_URL = None
    response = client.get("/")
    assert "Link" not in response
