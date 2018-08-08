"""Tests for static assets."""

import pytest


@pytest.mark.parametrize('url', ['/favicon.ico',
                                 '/apple-touch-icon.png',
                                 '/apple-touch-icon-precomposed.png',
                                 '/apple-touch-icon-120x120.png',
                                 '/robots.txt',
                                 '/humans.txt'])
def test_static_asset(client, url):
    """Test that static assets are present."""
    response = client.get(url, follow_redirects=True)
    assert response.status_code == 200
