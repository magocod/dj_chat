Django Chat
===========
![Alt text](https://firebasestorage.googleapis.com/v0/b/django-237201.appspot.com/o/repo_tags%2Ftag_py_36_37.png?alt=media&token=54c1a277-f100-4e47-b5a7-09afe86c3550 "python_versions")
![Alt text](https://github.com/magocod/dj_chat/blob/master/repository_images/tags/code_style_black.svg "code_style")

basic chat application, using websockets

* web consumer url: https://ngchat-cbfe2.firebaseapp.com/
* demo url server: https://djchat.herokuapp.com/

## Tox env

* Python 3.7
* Python 3.8
* Python lint flake8 (py3.8)

## Framework

* Django -> https://www.djangoproject.com/
* Channels -> https://channels.readthedocs.io/en/latest/index.html

## third-party

* Django-rest-framework -> https://www.django-rest-framework.org/
* black -> https://black.readthedocs.io/en/stable/
* isort -> https://timothycrosley.github.io/isort/

## Tests (98% coverage)

* Pytest -> https://docs.pytest.org/en/latest/
* coverage -> https://coverage.readthedocs.io/en/coverage-5.0.3/

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
