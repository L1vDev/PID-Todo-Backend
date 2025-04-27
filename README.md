# PID-Todo-Backend

## Index
1. [Description](#description)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Execution](#execution)

---

## Description
PID-Todo-Backend is an application for managing tasks and projects. This backend is developed with Django and Django Rest Framework, uses PostgreSQL as the database, and Poetry as the dependency manager.

---

## Prerequisites
Before you begin, make sure you have the following components installed on your system:
- Python 3.12 or higher
- PostgreSQL (You can also use SQLite3)
- Poetry or PIP
- Git

---

## Installation

1. **Clone the repository:**
   ```bash
   git clone git@github.com:L1vDev/PID-Todo-Backend.git
   cd pid-todo-backend
   ```
2. **Create a virtual environment**

    2.1 Using Poetry = 2.0:
    ```bash
    poetry env activate
    poetry install
    ```
    2.3 Using PIP on Windows:
    ```bash
    python -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt
    ```
    2.4 Using PIP on MacOS/Linux:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```
---
## Configuration
1. Create a `.env` file in the root of the project based on the `.env.example` file:
    ```bash
    cp .env.example .env
    ```
2. Edit the `.env` file with the appropriate values:
* `SECRET_KEY`: Type: String. This is a unique key used for cryptographic signing in Django, crucial for security. For example, `SECRET_KEY=your_secret_key`. To generate a new secret key, use this command in the shell:
    ```bash
    python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
    ```
    Copy and paste the generated key into the `.env` file.
* `DEBUG`: Type: Boolean, format: (True or False). This variable is used to set the debug mode of the application. For example, `DEBUG=False`.
* `HOSTS`: Type: String, format: hostname.com,localhost:5173,127.0.0.1. These are the hosts that the application can run on. For example, `HOSTS=example.com,localhost:5173,127.0.0.1:8000`.
* `SCHEMES`: Type: String, format: 'http://','https://'. These are the schemes that the application can run on. For example, `SCHEMES=https,http`.
* `DATABASE_ENGINE`: Type: String. This is the engine of the database. For example, `DATABASE_ENGINE=sqlite`. If you set `sqlite` as the engine, then you will not need the rest of the settings, otherwise, the engine will be PostgreSQL.
* `DATABASE_NAME`: Type: String. This is the name of the Postgres database. For example, `DATABASE_NAME=postgres`.
* `DATABASE_USER`: Type: String. This is the username for the Postgres database. For example, `DATABASE_USER=postgres`.
* `POSTGRES_HOST`: Type: String. This is the host for the Postgres database. For example, `POSTGRES_HOST=localhost`.
* `POSTGRES_PORT`: Type: String. This is the port for the Postgres database. For example, `POSTGRES_PORT=5432`.
* `POSTGRES_PASSWORD`: Type: String. This is the password for the Postgres database. For example, `POSTGRES_PASSWORD=postgres_password`.
* `EMAIL_HOST`: Type: String. This is the host for the email server. For example, `EMAIL_HOST=smtp.gmail.com`.
* `EMAIL_HOST_USER`: Type: String, format: email. This is the email address for the email server. For example, `EMAIL_HOST_USER=your-email@gmail.com`.
* `EMAIL_HOST_PASSWORD`: Type: String. This is the password for the email server. For example, `EMAIL_HOST_PASSWORD=email_host_password`.
* `EMAIL_DEFAULT_FROM`: Type: String. This is the default email address used in the "From" field for outgoing emails. For example, `EMAIL_DEFAULT_FROM=noreply@example.com`.
---
## Execution
1. To run the migrations, execute the following command:
    ```bash
    sh entrypoint.sh
    ```
2. To start the server:

    2.1 In development (DEBUG=True)
    ```bash
    python manage.py runserver
    ```
    2.2 In production (DEBUG=False)
    ```bash
    gunicorn todo_pid.wsgi
    ```

---
