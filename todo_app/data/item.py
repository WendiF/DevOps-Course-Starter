from enum import Enum

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
