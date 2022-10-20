from flask import Flask, render_template, request, redirect
from flask.helpers import url_for
import requests
import os

from todo_app.authenticator.github import Authenticator
from todo_app.authenticator.user import User, Role
from functools import wraps

from .data.item import Status
from .data.view_model import ViewModel
from .data.mongo_db_client import MongoDbClient

from todo_app.flask_config import Config

from todo_app.data import mongo_db_client
from flask_login import LoginManager, login_required, login_user, current_user

from todo_app.data import view_model

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())
    mongo_db_client = MongoDbClient()

    login_manager = LoginManager()
    github_authenticator = Authenticator()

    def writer_role_required(func):
        @wraps(func)
        def role_check(*args, **kwargs):
            if os.getenv('LOGIN_DISABLED') == 'True' or current_user.role == Role.WRITER:
                return func(*args, **kwargs)
        return role_check

    @login_manager.unauthorized_handler
    def unauthenticated():
        return redirect(github_authenticator.login_redirect)

    @login_manager.user_loader
    def load_user(user_id):
        return User(user_id)

    @app.route('/')
    @login_required
    def index():
        items = mongo_db_client.get_items()
        item_view_model = ViewModel(items)
        if current_user.role == Role.WRITER:
            return render_template('writer_index.html', view_model = item_view_model)
        else:
            return render_template('reader_index.html', view_model = item_view_model)

    @app.route("/login/callback")
    def github_authenticator_callback():
        user = github_authenticator.get_user()
        login_user(user)
        return redirect(url_for('index'))

    @app.route('/add_item', methods=['POST'])
    @login_required
    @writer_role_required
    def add_new_item():
        mongo_db_client.add_item(request.form.get("title"))
        return redirect(url_for('index'))

    @app.route('/update_todos', methods=['POST'])
    @login_required
    @writer_role_required
    def update_todos():
        mongo_db_client.update_status_for_items(request.form.getlist("start-todo-item"), Status.IN_PROGRESS)
        mongo_db_client.update_status_for_items(request.form.getlist("complete-todo-item"), Status.DONE)
        mongo_db_client.remove_items_by_id(request.form.getlist("delete-todo-item"))
        return redirect(url_for('index'))

    def sort_todo_list(items):
        return sorted(items, key=lambda item: item.status, reverse=True)

    login_manager.init_app(app)

    return app