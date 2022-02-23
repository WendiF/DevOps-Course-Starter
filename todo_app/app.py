from flask import Flask, render_template, request, redirect
from flask.helpers import url_for

from .data.view_model import ViewModel
from .data.trello_items import get_items, add_item, mark_items_as_in_progress, mark_items_as_completed, remove_items_by_id

from todo_app.flask_config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())

    @app.route('/')
    def index():
        items = get_items()
        item_view_model = ViewModel(items)
        return render_template('index.html', view_model = item_view_model)

    @app.route('/add_item', methods=['POST'])
    def add_new_item():
        add_item(request.form.get("title"))
        return redirect(url_for('index'))

    @app.route('/update_todos', methods=['POST'])
    def update_todos():
        mark_items_as_in_progress(request.form.getlist("start-todo-item"))
        mark_items_as_completed(request.form.getlist("complete-todo-item"))
        remove_items_by_id(request.form.getlist("delete-todo-item"))
        return redirect(url_for('index'))

    def sort_todo_list(items):
        return sorted(items, key=lambda item: item.status, reverse=True)

    return app