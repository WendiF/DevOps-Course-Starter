from flask_login import UserMixin
from enum import Enum
import os
class Role(Enum):
    READER = "To Do"
    WRITER = "In Progress"

class User(UserMixin):
    def __init__(self, id):
        self.id = id

    @property
    def role(self):
        if self.id == os.getenv("TODO_WRITER"):
            return Role.WRITER
        return Role.READER