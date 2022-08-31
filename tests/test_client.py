import pytest
from dotenv import load_dotenv, find_dotenv
from todo_app import app
import os
import mongomock
from pymongo import MongoClient

from datetime import date

@pytest.fixture
def client():
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)

    with mongomock.patch(servers=(('fakemongo.com', 27017),)):
        test_app = app.create_app()
        with test_app.test_client() as client:
            yield client

@pytest.fixture
def items():
    client = MongoClient(os.getenv("MB_CONNECTION_STRING"))
    db = client[os.getenv("DATABASE_NAME")]
    return db.todo_app_collection
class StubResponse():
    def __init__(self, fake_response_data):
        self.fake_response_data = fake_response_data

    def json(self):
        return self.fake_response_data