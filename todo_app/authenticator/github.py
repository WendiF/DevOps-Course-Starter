import os
import requests
from flask import request
import uuid
from todo_app.authenticator.user import User

class Authenticator:

    def __init__(self):
        self.access_token = None

    @property
    def login_redirect(self):
        client_id = os.getenv('CLIENT_ID')
        return f'https://github.com/login/oauth/authorize?client_id={client_id}'   

    def get_access_token(self):
        access_token_request = requests.post(
            "https://github.com/login/oauth/access_token",
            params={
                "client_id": os.getenv('CLIENT_ID'),
                "client_secret": os.getenv('CLIENT_SECRET'),
                "code": request.values.get("code")
            },
            headers={"Accept": "application/json"}
        )
        self.access_token = access_token_request.json()["access_token"]

    def get_user(self):
        self.get_access_token()
        response = requests.get('https://api.github.com/user', 
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f'Bearer {self.access_token}'
        })
        return User(response.json()["id"])
        
 