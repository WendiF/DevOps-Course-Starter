import pytest

from todo_app.data.item import ApiItem, Status
from todo_app.data.view_model import ViewModel
from datetime import date, timedelta

def generate_test_items(start, end, status, is_past = False):
    return [ApiItem(id, 'Test ApiItem', status.value, date.today() - timedelta(days=1) if is_past else date.today()) for id in range(start, end + 1)]

to_do_ApiItems = []
in_progress_ApiItems = generate_test_items(1, 1, Status.IN_PROGRESS)
done_ApiItems = generate_test_items(2, 4, Status.DONE)
all_ApiItems = to_do_ApiItems + in_progress_ApiItems + done_ApiItems

@pytest.fixture
def view_model() -> ViewModel:
    return ViewModel(all_ApiItems)

def test_view_model_returns_all_ApiItems(view_model: ViewModel):
    assert view_model.ApiItems == all_ApiItems

def test_view_model_returns_to_do_ApiItems(view_model: ViewModel):
    assert view_model.to_do_ApiItems == to_do_ApiItems

def test_view_model_returns_in_progress_ApiItems(view_model: ViewModel):
    assert view_model.in_progress_ApiItems == in_progress_ApiItems

def test_view_model_returns_done_ApiItems(view_model: ViewModel):
    assert view_model.done_ApiItems == done_ApiItems
    
def test_view_model_returns_should_show_all_done_ApiItems_returns_true_for_fewer_than_five_tasks(view_model: ViewModel):
    assert view_model.should_show_all_done_ApiItems == True
    
def test_view_model_returns_should_show_all_done_ApiItems_returns_false_for_more_than_five_tasks():
    view_model = ViewModel(done_ApiItems + generate_test_items(5, 9, Status.DONE))
    assert view_model.should_show_all_done_ApiItems == False
    
def test_view_model_returns_recent_done_ApiItems(view_model: ViewModel):
    assert view_model.recent_done_ApiItems == done_ApiItems
    
def test_view_model_returns_older_done_ApiItems(view_model: ViewModel):
    view_model = ViewModel(generate_test_items(10, 16, Status.DONE, True))
    assert view_model.older_done_ApiItems == view_model.older_done_ApiItems
