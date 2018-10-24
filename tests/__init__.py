import pytest


@pytest.fixture()
def client(mocker):
    return mocker.Mock(url_root='https://api.example.com')
