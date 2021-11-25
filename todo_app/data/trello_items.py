from enum import Enum
from typing import ParamSpec
import requests
import os

class Status(Enum):
    NOT_STARTED = "Not Started"
    COMPLETED = "Completed"

API_URL = "https://api.trello.com"
TOKEN = os.getenv('TOKEN')
SECRET_KEY = os.getenv('SECRET_KEY')
BOARD_ID = os.getenv('BOARD_ID')
BASE_PAYLOAD = {
        'key': SECRET_KEY,
        'token': TOKEN
    }

def get_items():
    payload = {**BASE_PAYLOAD, 'cards': 'open'}
    r = requests.get(f'https://api.trello.com/1/boards/{BOARD_ID}/lists', params = payload)
    items = map_json_to_items(r.json())
    return items

def add_item(title):
    list_ids = map_lists_to_statuses()
    payload = {**BASE_PAYLOAD, 'name': title, 'idList': list_ids[Status.NOT_STARTED]
    }
    requests.post('https://api.trello.com/1/cards', params = payload)

def mark_items_as_completed(ids):
    list_ids = map_lists_to_statuses()
    for id in ids:
        payload = {**BASE_PAYLOAD, 'idList': list_ids[Status.COMPLETED]}
        requests.put(f'https://api.trello.com/1/cards/{id}', params = payload)

def remove_items_by_id(ids):
    for id in ids:
        payload = {
            'key': SECRET_KEY,
            'token': TOKEN,
        }
        requests.delete(f'https://api.trello.com/1/cards/{id}', params = payload)

def map_lists_to_statuses():
    lists = requests.get(f'https://api.trello.com/1/boards/{BOARD_ID}/lists', params = BASE_PAYLOAD).json()

    list_ids = {list['name']: list['id'] for list in lists}
    list_ids[Status.NOT_STARTED] = list_ids.pop('To Do')
    list_ids[Status.COMPLETED] = list_ids.pop('Done')

    return list_ids

def map_json_to_items(json):
    to_do_cards = next((list for list in json if list['name'] == 'To Do'), None)['cards']
    to_do_items = [{'id': card['id'], 'status': Status.NOT_STARTED.value, 'title': card['name']} for card in to_do_cards]

    done_cards = next((list for list in json if list['name'] == 'Done'), None)['cards']
    done_items = [{'id': card['id'], 'status': Status.COMPLETED.value, 'title': card['name']} for card in done_cards]

    return to_do_items + done_items