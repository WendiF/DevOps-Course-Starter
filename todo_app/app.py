from flask import Flask, render_template, request, redirect
from flask.helpers import url_for
from .data.trello_items import get_items, add_item, mark_items_as_completed, remove_items_by_id

from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():
    items = get_items()
    return render_template('index.html', items = sort_todo_list(items))

@app.route('/add_item', methods=['POST'])
def add_new_item():
    add_item(request.form.get("title"))
    return redirect(url_for('index'))

@app.route('/update_todos', methods=['POST'])
def update_todos():
    mark_items_as_completed(request.form.getlist("complete-todo-item"))
    remove_items_by_id(request.form.getlist("delete-todo-item"))
    return redirect(url_for('index'))

def sort_todo_list(items):
    return sorted(items, key=lambda item: item['status'], reverse=True)