import pytest
from dotenv import load_dotenv, find_dotenv
from todo_app import app
import os

from todo_app.data.item import Item, Status
from datetime import date

import pymongo
import mongomock
import pytest

from pymongo.collection import Collection

from todo_app.data.item import ApiItem


class StubResponse():
    def __init__(self, fake_response_data):
        self.fake_response_data = fake_response_data

    def json(self):
        return self.fake_response_data

@pytest.fixture
def client():
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)

    with mongomock.patch(servers=(('fakemongo.com', 27017),)):
        test_app = app.create_app()
        with test_app.test_client() as client:
            yield client

@pytest.fixture
def items() -> Collection:
    client = pymongo.MongoClient(os.getenv("PRIMARY_CONNECTION_STRING"))
    db = client[os.getenv("DATABASE_NAME")]
    return db.todo_app_collection

def test_index_page(client, items):
    add_test_items(items)
    response = client.get('/')
    assert response.status_code == 200
    assert 'Test Item' in response.data.decode() 

def add_test_items(items: Collection):
    items.insert_one(Item('Test Item').__dict__)
