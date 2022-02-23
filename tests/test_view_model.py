import pytest

from todo_app.data.item import Item, Status
from todo_app.data.view_model import ViewModel
from datetime import date, timedelta

def generate_test_items(start, end, status, is_past = False):
    return [Item(id, 'Test Item', status.value, date.today() - timedelta(days=1) if is_past else date.today()) for id in range(start, end + 1)]

to_do_items = []
in_progress_items = generate_test_items(1, 1, Status.IN_PROGRESSS)
done_items = generate_test_items(2, 4, Status.DONE)
all_items = to_do_items + in_progress_items + done_items

@pytest.fixture
def view_model() -> ViewModel:
    return ViewModel(all_items)

def test_view_model_returns_all_items(view_model: ViewModel):
    assert view_model.items == all_items

def test_view_model_returns_to_do_items(view_model: ViewModel):
    assert view_model.to_do_items == to_do_items

def test_view_model_returns_in_progress_items(view_model: ViewModel):
    assert view_model.in_progress_items == in_progress_items

def test_view_model_returns_done_items(view_model: ViewModel):
    assert view_model.done_items == done_items
    
def test_view_model_returns_should_show_all_done_items_returns_true_for_fewer_than_five_tasks(view_model: ViewModel):
    assert view_model.should_show_all_done_items == True
    
def test_view_model_returns_should_show_all_done_items_returns_false_for_more_than_five_tasks():
    view_model = ViewModel(done_items + generate_test_items(5, 9, Status.DONE))
    assert view_model.should_show_all_done_items == False
    
def test_view_model_returns_recent_done_items(view_model: ViewModel):
    assert view_model.recent_done_items == done_items
    
def test_view_model_returns_older_done_items(view_model: ViewModel):
    view_model = ViewModel(generate_test_items(10, 16, Status.DONE, True))
    assert view_model.older_done_items == view_model.older_done_items
