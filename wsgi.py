import dotenv
from todo_app.app import create_app

def run():
    dotenv.load_dotenv()
    return create_app()