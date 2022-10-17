from enum import Enum
from datetime import date

class Status(Enum):
    TO_DO = "To Do"
    IN_PROGRESS = "In Progress"
    DONE = "Done"

class ApiItem:
    def __init__(self, id, title, status = Status.TO_DO.value, date_last_activity = date.today()):
        self.id = id
        self.title = title
        self.status = status
        self.date_last_activity = date_last_activity
    
    @classmethod
    def from_json(cls, json):
        return cls(json['_id'], json['title'], json['status'], json['date_last_activity'])

class Item:
    def __init__(self, title):
        self.title = title
        self.status = Status.TO_DO.value
        self.date_last_activity = date.today().isoformat()