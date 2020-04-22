Intro and Quick Start
*********************

Intro
=====

The sample project. explains how to implement a django application in real time
    
    * Framework .. _Django: https://www.djangoproject.com/
    * Websockests .. _channels: https://github.com/django/channels


Quick Start
===========


**Recommended:**

* python >= 3.7
* tox >= 3.14


1. Create a virtual python environment and install libraries with pip

.. code:: python

    pip install -r requirements.txt

2. Migrate the database.

.. code:: python

    python manage.py migrate

3. python manage.py runserver, Enter the address http://localhost:8000

.. code:: python

    python manage.py runserver

4. Create all virtual environments (using tox)

.. code:: python

	tox