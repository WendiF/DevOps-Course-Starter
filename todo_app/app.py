from flask import Flask, render_template, request, redirect
from flask.helpers import url_for

from .data.item import Status
from .data.view_model import ViewModel
from .data.mongo_db_client import MongoDbClient

from todo_app.flask_config import Config

from todo_app.data import mongo_db_client

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())
    mongo_db_client = MongoDbClient()

    @app.route('/')
    def index():
        items = mongo_db_client.get_items()
        item_view_model = ViewModel(items)
        return render_template('index.html', view_model = item_view_model)

    @app.route('/add_item', methods=['POST'])
    def add_new_item():
        mongo_db_client.add_item(request.form.get("title"))
        return redirect(url_for('index'))

    @app.route('/update_todos', methods=['POST'])
    def update_todos():
        mongo_db_client.update_status_for_items(request.form.getlist("start-todo-item"), Status.IN_PROGRESS)
        mongo_db_client.update_status_for_items(request.form.getlist("complete-todo-item"), Status.DONE)
        mongo_db_client.remove_items_by_id(request.form.getlist("delete-todo-item"))
        return redirect(url_for('index'))

    def sort_todo_list(items):
        return sorted(items, key=lambda item: item.status, reverse=True)

    return app