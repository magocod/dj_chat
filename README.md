# Django Chat

* Demo url: https://djchat.herokuapp.com/

## Tox env

* Python 3.7
* Python 3.8
* Python lint flake8 (py3.8)

## Framework

* Django -> https://www.djangoproject.com/
* Channels -> https://channels.readthedocs.io/en/latest/index.html

## third-party

* Django-rest-framework -> https://www.django-rest-framework.org/

## Tests (99% coverage)

* Pytest -> https://docs.pytest.org/en/latest/

## Instructions

Create a virtual python environment and install libraries with pip

```bash
pip install -r requirements.txt
```

Create all virtual environments (using tox)
```bash
tox
```

Migrate the database

```bash
python manage.py migrate
```

run tests (verify successful installation)
```bash
pytest
```

run tests (verify coverage)
```bash
pytest --cov
```

Run development server

```bash
python manage.py runserver
```

Enter the address

```bash
http://localhost:8000
```
