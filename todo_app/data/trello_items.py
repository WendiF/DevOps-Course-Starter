from enum import Enum
import requests
import os

API_URL = "https://api.trello.com"
BOARD_ID = os.getenv('BOARD_ID')
BASE_PAYLOAD = {
    'key': os.getenv('API_KEY'),
    'token': os.getenv('TOKEN')
}
class Status(Enum):
    TO_DO = "To Do"
    DONE = "Done"

class Item:
    def __init__(self, id, title, status = Status.TO_DO.value):
        self.id = id
        self.title = title
        self.status = status
    
    @classmethod
    def from_trello_card(cls, card, list):
        return cls(card['id'], card['name'], list['name'])

def get_items():
    payload = {**BASE_PAYLOAD, 'cards': 'open'}
    response = requests.get(f'{API_URL}/1/boards/{BOARD_ID}/lists', params = payload).json()
    items = map_lists_with_cards_to_items(response)
    return items

def add_item(title):
    list_ids = map_lists_to_statuses()
    payload = {**BASE_PAYLOAD, 'name': title, 'idList': list_ids[Status.TO_DO.value]}
    requests.post(f'{API_URL}/1/cards', params = payload)

def mark_items_as_completed(ids):
    list_ids = map_lists_to_statuses()
    for id in ids:
        payload = {**BASE_PAYLOAD, 'idList': list_ids[Status.DONE.value]}
        requests.put(f'{API_URL}/1/cards/{id}', params = payload)

def remove_items_by_id(ids):
    for id in ids:
        requests.delete(f'{API_URL}/1/cards/{id}', params = BASE_PAYLOAD)

def map_lists_to_statuses():
    lists = requests.get(f'{API_URL}/1/boards/{BOARD_ID}/lists', params = BASE_PAYLOAD).json()
    list_ids = {list['name']: list['id'] for list in lists}
    return list_ids

def map_lists_with_cards_to_items(card_lists):
    items = []
    for card_list in card_lists:
        items.extend([Item.from_trello_card(card, card_list) for card in card_list['cards']])
    return items