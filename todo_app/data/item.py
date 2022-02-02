from enum import Enum
from datetime import date

class Status(Enum):
    TO_DO = "To Do"
    IN_PROGRESSS = "In Progress"
    DONE = "Done"

class Item:
    def __init__(self, id, title, status = Status.TO_DO.value, date_last_activity = date.today()):
        self.id = id
        self.title = title
        self.status = status
        self.date_last_activity = date_last_activity
    
    @classmethod
    def from_trello_card(cls, card, list):
        return cls(card['id'], card['name'], list['name'], date.fromisoformat(card['dateLastActivity'].split('T')[0]))
