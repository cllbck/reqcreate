from reqcreate.main import get_all_files, find_packages_from_file, get_all_packages, \
    clear_bultins_packages, create_requirements_file
import pytest
import os
import shutil
import requests
import json

main_dir = os.path.join(os.path.dirname(__file__), 'test_data')
child_dir = os.path.join(main_dir, 'test_data_child')
main_file = os.path.join(main_dir, 'main.py')
child_file = os.path.join(child_dir, 'child.py')
child_wrong_file = os.path.join(child_dir, 'virus.dmg')


class MockResponse:

    @property
    def content(self):
        return json.dumps({
            'info': {
                'name': 'Flask',
                'version': '1.1.1'
            },
            'releases': {
            }
        })

    @property
    def status_code(self):
        return 200

@pytest.fixture
def mock_response(monkeypatch):

    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)

def setup_module():
    os.mkdir(main_dir)
    os.mkdir(child_dir)
    with open(main_file, 'w+') as f:
        f.write('import json\n')
        f.write('import flask\n')
        f.write('from datetime import datetime\n')
        f.write('from werkzeug.security import generate_password_hash, check_password_hash\n')
    with open(child_file, 'w+') as f:
        f.write('import geojson\n')
        f.write('from bson.objectid import ObjectId\n')
        f.write('from random import randint\n')
        f.write('from celery.schedules import crontab\n')
    with open(child_wrong_file, 'w+') as f:
        f.write('Created by pytest\n')


def teardown_module():
    shutil.rmtree(main_dir)


def test_get_all_files():
    assert get_all_files(main_dir) == [main_file, child_file]


def test_find_packages_from_file():
    assert find_packages_from_file(child_file) == ['geojson', 'bson', 'random', 'celery']
    assert find_packages_from_file(main_file) == ['json', 'flask', 'datetime', 'werkzeug']


def test_get_all_packages():
    all_files = [main_file, child_file]
    assert get_all_packages(all_files) == {'json', 'flask', 'random', 'werkzeug', 'datetime', 'geojson', 'celery',
                                           'bson'}


def test_clear_bultin_packages():
    assert clear_bultins_packages({'json', 'flask', 'random', 'werkzeug', 'datetime', 'geojson', 'celery', 'bson'}) == {
         'flask', 'werkzeug', 'geojson', 'celery', 'bson'}


def test_create_requirements_file(mock_response):
    create_requirements_file(['flask'], main_dir)
    req_file = os.path.join(main_dir, 'requirements.txt')
    assert os.path.isfile(req_file) == True
    with open(req_file, 'r') as f:
        data = f.read().strip('\n')
    assert data == 'Flask==1.1.1'