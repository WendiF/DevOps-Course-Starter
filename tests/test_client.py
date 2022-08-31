import pytest
from dotenv import load_dotenv, find_dotenv
from todo_app import app
import os
import requests
import mongomock

from datetime import date
from todo_app.data.mongo_db_client import get_items

@pytest.fixture
def client():
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)

    with mongomock.patch(servers=(('fakemongo.com', 27017),)):
        test_app = app.create_app()
        with test_app.test_client() as client:
            yield client

def test_index_page(monkeypatch, client):
    monkeypatch.setattr(requests, 'get', get_items)
    response = client.get('/')
    assert response.status_code == 200
    assert 'Test card' in response.data.decode() 

class StubResponse():
    def __init__(self, fake_response_data):
        self.fake_response_data = fake_response_data

    def json(self):
        return self.fake_response_data
    
def get_items(url, params):
    test_board_id = os.environ.get('BOARD_ID')
    fake_response_data = None
    if url == f'https://api.trello.com/1/boards/{test_board_id}/lists':
        fake_response_data = [{
            'id': '123abc',
            'name': 'To Do',
            'cards': [{'id': '456', 'name': 'Test card', 'dateLastActivity': f'{date.today()}'}]
        }]
    return StubResponse(fake_response_data)