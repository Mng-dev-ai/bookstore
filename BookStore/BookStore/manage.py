import click
from flask.cli import with_appcontext
import csv
from sqlalchemy import create_engine
from BookStore.config import SQLALCHEMY_DATABASE_URI
import os

engine = create_engine(SQLALCHEMY_DATABASE_URI)
csv_path = os.path.dirname(__file__)  + '/../books.csv'

@click.command("init")
@with_appcontext
def init():
    from BookStore.extensions import db
    from BookStore.models import Book

    click.echo("creating the books")
    with open(csv_path,'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            book = Book(
                isbn=row["isbn"],
                title=row["title"],
                author_first_name=row["author_first_name"],
                author_last_name=row["author_last_name"],
                page_count=row["page_count"],
                description=row["description"],
            )
            db.session.add(book)
    db.session.commit()
    click.echo("created the books")
