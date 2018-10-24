# -*- coding=utf8 -*-
import pytest

from productai import Client
from productai.bad_case import BadCaseApi

from . import client


def test_get_test_case_api():
    cli = Client('', '')
    api = cli.get_bad_case_api()
    assert isinstance(api, BadCaseApi)
    assert api.client == cli


def test_add_test_case(client, mocker):
    api = BadCaseApi(client)

    api.add('1', '2')
    api.client.post.assert_called_with(
        api.base_url,
        data={'service_id': '1', 'request_id': '2'},
    )

    api.add('1', '2', description='test', details=dict(c=3))
    api.client.post.assert_called_with(
        api.base_url,
        data={'service_id': '1', 'request_id': '2', 'description': 'test', 'details': { 'c': 3 }},
    )
