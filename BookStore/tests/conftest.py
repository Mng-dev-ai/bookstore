import json
import pytest
from dotenv import load_dotenv

from BookStore.models import Book
from BookStore.app import create_app
from BookStore.extensions import db as _db
from pytest_factoryboy import register
from tests.factories import BookFactory


register(BookFactory)


@pytest.fixture(scope="session")
def app():
    load_dotenv(".testenv")
    app = create_app(testing=True)
    return app


@pytest.fixture
def db(app):
    _db.app = app

    with app.app_context():
        _db.create_all()

    yield _db

    _db.session.close()
    _db.drop_all()
