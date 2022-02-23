from todo_app.data.item import Status
from datetime import date

class ViewModel: 
    def __init__(self, items):
        self._items = items

    @property
    def items(self):
        return self._items

    @property
    def to_do_items(self):
        return list(filter(lambda item: item.status == Status.TO_DO.value, self._items))

    @property
    def in_progress_items(self):
        return list(filter(lambda item: item.status == Status.IN_PROGRESSS.value, self._items))

    @property
    def done_items(self):
        return list(filter(lambda item: item.status == Status.DONE.value, self._items))

    @property
    def should_show_all_done_items(self):
        return len(self.done_items) < 5

    @property
    def recent_done_items(self): 
        return list(filter(lambda item: (item.date_last_activity == date.today()), self.done_items))

    @property
    def older_done_items(self):
        return list(filter(lambda item: item.date_last_activity != date.today(), self.done_items))
        