"""Tests for static assets."""

import pytest


@pytest.mark.parametrize("url", ["/favicon.ico", "/robots.txt", "/humans.txt"])
def test_static_asset(client, url):
    """Test that static assets are present."""
    response = client.get(url, follow_redirects=True)
    assert response.status_code == 200
