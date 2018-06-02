"""Board tests."""

import pytest

import factories


@pytest.fixture
def roll():
    return factories.RollFactory()


@pytest.mark.django_db
@pytest.mark.parametrize('url', ['/'])
def test_public(client, url):
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.parametrize('url', ['/roll/'])
def test_requires_auth(client, admin_client, url, roll):
    response = client.get(url)
    assert response.status_code == 302
    response = admin_client.get(url)
    assert response.status_code == 200

