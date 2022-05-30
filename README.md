# DevOps Apprenticeship: Project Exercise

## System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.7+ and install Poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

### Poetry installation (Bash)

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -
```

### Poetry installation (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py -UseBasicParsing).Content | python -
```

## Dependencies

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from your preferred shell:

```bash
$ poetry install
```

You'll also need to clone a new `.env` file from the `.env.template` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change). There's also a [SECRET_KEY](https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie. 

You will also need to set the variables API_KEY, TOKEN, BOARD_ID in `.env`. Sign up for a Trello account, and create a new board with lists named 'To Do' and 'Done'. You can get your API_KEY and TOKEN by following the [instructions here](https://trello.com/app-key). You can get your BOARD_ID by adding '.json' to the end of your Trello board url, and finding the field called 'idList'.

## Running the App

Once the all dependencies have been installed, start the Flask app in development mode within the Poetry environment by running:
```bash
$ poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

## Running the App with Ansible
Move the files `my-ansible-playbook`, `create-todo-app.yaml` and `.env.j2` to the control node, install ansible, and run
```
ansible-playbook my-ansible-playbook.yaml -i my-ansible-inventory
```
## Running Tests
This To-Do App is tested with pytest. Once the all dependencies have been installed, run all tests within the Poetry environment by running:
```bash
$ poetry run pytest
```
Test files exist within the `tests` folder, with test files labelled `test_....py`. 
To run a specific test file, run: 
```bash
$ poetry run pytest path/to/test_file.py
```

## Architecture Diagrams

### Context Diagram
![Context Diagram](./documentation/context_diagram.drawio.png)
### Container Diagram
![Container Diagram](./documentation/container_diagram.drawio.png)
### Component Diagram
![Component Diagram](./documentation/component_diagram.drawio.png)
### Code Diagram
![Code Diagram](./documentation/code_diagram.png)
