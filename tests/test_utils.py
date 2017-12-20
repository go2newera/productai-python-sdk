# -*- coding:utf-8 -*-
import datetime as dt

import pytest

import productai as m


def test_date_str():
    d = dt.datetime(2015, 1, 11, 12, 13, 14)
    assert m.date_str(d) == '2015-01-11T12:13:14Z'
    with pytest.raises(ValueError):
        m.date_str('asdfasdf')
    assert m.date_str(dt.datetime(2017, 2, 10, 12, 13, 14)) == '2017-02-10T12:13:14Z'
