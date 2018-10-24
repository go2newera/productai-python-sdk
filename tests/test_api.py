import csv
import json
import pytest

import productai as m

from . import client


class TestQuery:

    def test_should_upload_file_like_obj(self, client, mocker):
        api = m.API(client, 'classify_fashion', '_0000001')
        f = mocker.Mock()
        f.read = lambda: b'1111'

        api.query(f, '0-0-1-1')

        api.client.post.assert_called_with(
            api.base_url,
            data={'loc': '0-0-1-1', 'count': 20},
            files={'search': f}
        )

    def test_should_accept_image_url(self, client, mocker):
        api = m.API(client, 'classify_fashion', '_0000001')
        image = 'http://httpbin.org/image'

        api.query(image, '0-0-1-1')

        api.client.post.assert_called_with(
            api.base_url,
            data={'loc': '0-0-1-1', 'url': image, 'count': 20},
            files=None,
        )

    def test_search_with_option(self, client, mocker):
        url = 'http://httpbin.org/image'
        api = m.API(client, 'search', '******')

        api.query(url)
        api.client.post.assert_called_with(
            api.base_url,
            data={'loc': '0-0-1-1', 'url': url, 'count': 20},
            files=None
        )

        api.query(url, abc=123)
        api.client.post.assert_called_with(
            api.base_url,
            data={'loc': '0-0-1-1', 'url': url, 'count': 20, 'abc': 123},
            files=None
        )

        with pytest.raises(ValueError) as val_err:
            api.query(url, search='123')
        assert str(val_err.value) == "The keys ['search'] are in conflict with built-in parameters."

    def test_search_by_tag(self, client, mocker):
        url = 'http://httpbin.org/image'
        api = m.API(client, 'search', '******')

        api.query(url, tags=None)
        api.client.post.assert_called_with(
            api.base_url,
            data={'loc': '0-0-1-1', 'url': url, 'count': 20},
            files=None
        )

        api.query(url, tags='1')
        api.client.post.assert_called_with(
            api.base_url,
            data={'loc': '0-0-1-1', 'url': url, 'count': 20, 'tags': '1'},
            files=None
        )

        api.query(url, tags='1|2')
        api.client.post.assert_called_with(
            api.base_url,
            data={'loc': '0-0-1-1', 'url': url, 'count': 20, 'tags': '1|2'},
            files=None
        )

        api.query(url, tags=['1'])
        api.client.post.assert_called_with(
            api.base_url,
            data={'loc': '0-0-1-1', 'url': url, 'count': 20, 'tags': '1'},
            files=None
        )

        api.query(url, tags=['1', '2', '3'])
        api.client.post.assert_called_with(
            api.base_url,
            data={'loc': '0-0-1-1', 'url': url, 'count': 20, 'tags': '1|2|3'},
            files=None
        )

        expected = {'or': ['1', '2']}
        api.query(url, tags=expected)
        api.client.post.assert_called_with(
            api.base_url,
            data={'loc': '0-0-1-1', 'url': url, 'count': 20, 'tags': json.dumps(expected)},
            files=None
        )

        expected = {
            'or': [
                '1',
                '2',
                {'and': ['3', '4']},
                {'or': ['5', {'and': ['7', '8']}]}
            ]
        }
        api.query(url, tags=expected)
        api.client.post.assert_called_with(
            api.base_url,
            data={'loc': '0-0-1-1', 'url': url, 'count': 20, 'tags': json.dumps(expected)},
            files=None
        )


class TestNormalizeImagesFile:

    def test_should_accept_file_name(self, tmpdir):
        csv_row = "http://x.com/a.jpg,12,good"
        f = tmpdir.mkdir('images').join('bulk1.csv')
        f.write(csv_row)
        with m._normalize_items_file(str(f)) as r:
            assert r.read() == csv_row

    def test_should_return_file_as_it_is(self, tmpdir):
        csv_row = "http://x.com/a.jpg,12,good"
        tf = tmpdir.mkdir('images').join('bulk1.csv')
        tf.write(csv_row)
        with open(str(tf)) as f:
            with m._normalize_items_file(f) as r:
                assert r == f

    def test_should_create_tmp_file(self, tmpdir):
        imgs_info = [
            ['http://x.com/a.jpg', '12', 'good'],
            ['http://x.com/b.jpg', '13', 'bad'],
        ]
        with m._normalize_items_file(imgs_info, tmpdir=str(tmpdir)) as f:
            reader = csv.reader(f)
            assert list(reader) == imgs_info
            assert tmpdir.listdir()
        assert not tmpdir.listdir()


class TestCreateImageSet:

    def test_create_image_set(self, client):
        name, description = 'image set name', 'a description'
        api = m.ImageSetAPI(client)
        api.create_image_set(name=name)
        api.client.post.assert_called_with(api.base_url, json={'name': name})

        api.create_image_set(name=name, description=description)
        api.client.post.assert_called_with(api.base_url, json={
            'name': name,
            'description': description,
        })


class TestGetImageSets:

    def test_get_image_sets(self, client):
        api = m.ImageSetAPI(client)
        api.get_image_sets()
        api.client.get.assert_called_with(api.base_url)


class TestGetAllServicesInfo:

    def test_get_all_services_info(self, client):
        api = m.CustomerServiceAPI(client)
        api.get_services()
        api.client.get.assert_called_with(api.base_url)
