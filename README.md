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

You will also need to set the variables PRIMARY_CONNECTION_STRING and DATABASE_NAME in `.env`.

## Running the App with Ansible
Move the files `my-ansible-playbook`, `create-todo-app.yaml` and `.env.j2` to the control node, install ansible, and run
```
ansible-playbook my-ansible-playbook.yaml -i my-ansible-inventory
```

## Running and Testing the App with Docker Compose
You can run 

```
docker-compose up
```

to build and run tests for the todo app in development mode.

## Running the App with Docker in Production
You can build and run the Docker Image with the following commands: 

```
docker build --target production --tag todo_app:prod .
docker run -d -p 5000:80 --env-file ./.env todo_app:prod .
```

Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

## Viewing the App on Production
You can view the todo app on the following hosting site: 
[`https://todo-app-by-wendi.azurewebsites.net/`](https://todo-app-by-wendi.azurewebsites.net/)

## Running the App with Docker in Development
You can build and run the Docker Image with the following commands: 

```
docker build --target development --tag todo_app:dev .
docker run -d -p 5000:5000 --env-file ./.env --mount type=bind,source="$(pwd)"/todo_app,target=/todo_app/todo_app todo_app:dev
```

Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app. Any changes you make in the codebase will automatically be updated here.

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
