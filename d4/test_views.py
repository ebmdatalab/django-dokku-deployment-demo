import pytest

from d4.models import Thing


@pytest.mark.django_db
def test_get_index(client):
    Thing.objects.create(name="aardvark")
    rsp = client.get("/")
    assert rsp.status_code == 200
    assert b"aardvark" in rsp.content
