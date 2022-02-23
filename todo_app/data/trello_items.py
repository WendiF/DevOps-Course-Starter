from .item import Status, Item
import requests
import os

API_URL = "https://api.trello.com"

def get_base_payload():
    return {
        'key': os.getenv('API_KEY'),
        'token': os.getenv('TOKEN')
    }

def get_board_id():
    return os.getenv('BOARD_ID')

def get_items():
    payload = {**get_base_payload(), 'cards': 'open'}
    response = requests.get(f'{API_URL}/1/boards/{get_board_id()}/lists', params = payload).json()
    items = map_lists_with_cards_to_items(response)
    return items

def add_item(title):
    list_ids = map_lists_to_statuses()
    payload = {**get_base_payload(), 'name': title, 'idList': list_ids[Status.TO_DO.value]}
    requests.post(f'{API_URL}/1/cards', params = payload)

def mark_items_as_in_progress(ids):
    list_ids = map_lists_to_statuses()
    for id in ids:
        payload = {**get_base_payload(), 'idList': list_ids[Status.IN_PROGRESSS.value]}
        requests.put(f'{API_URL}/1/cards/{id}', params = payload)

def mark_items_as_completed(ids):
    list_ids = map_lists_to_statuses()
    for id in ids:
        payload = {**get_base_payload(), 'idList': list_ids[Status.DONE.value]}
        requests.put(f'{API_URL}/1/cards/{id}', params = payload)

def remove_items_by_id(ids):
    for id in ids:
        requests.delete(f'{API_URL}/1/cards/{id}', params = get_base_payload())

def map_lists_to_statuses():
    lists = requests.get(f'{API_URL}/1/boards/{get_board_id()}/lists', params = get_base_payload()).json()
    list_ids = {list['name']: list['id'] for list in lists}
    return list_ids

def map_lists_with_cards_to_items(card_lists):
    items = []
    for card_list in card_lists:
        items.extend([Item.from_trello_card(card, card_list) for card in card_list['cards']])
    return items