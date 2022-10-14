from .item import Item, ApiItem
import os
from pymongo import MongoClient
from datetime import date

class MongoDbClient:
    def __init__(self):
        client = MongoClient(os.getenv('PRIMARY_CONNECTION_STRING'))
        db = client[os.getenv('DATABASE_NAME')]
        self.items = db.todo_app_collection

    def get_items(self):
        return [ApiItem.from_json(item) for item in self.items.find()]

    def add_item(self, title):
        new_item = Item(title).__dict__
        self.items.insert_one(new_item)

    def update_status_for_items(self, ids, status):
        for id in ids:
            self.items.find_one_and_update({'_id': id}, { '$set': {'status': status.value, 'date_last_activity': date.today().isoformat()}})

    def remove_items_by_id(self, ids):
        self.items.delete_many({'_id': { '$in': ids}})