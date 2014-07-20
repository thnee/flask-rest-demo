
# flask-rest-demo

The purpose of this repo is only to demonstrate how to build a simple REST API with Flask.

## Installation

I recommend using `virtualenv` and `virtualenvwrapper` to isolate packages.

Use pip to install the packages in the requirements file:

```
$ pip install -r requirements.txt
```

## Initializing the db

To run the app, the database must be initialized:

```
$ python
>>> from app import db
>>> db.create_all()
```

## Running the app

Just run the included script using python:

```
$ python runserver.py
```
