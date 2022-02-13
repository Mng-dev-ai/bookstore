from flask import url_for
from BookStore.models import Book


def test_get_book(client, db, book):
    # test 404
    book_url = url_for('api.book_by_id', book_id="10000")
    rep = client.get(book_url)
    assert rep.status_code == 404

    db.session.add(book)
    db.session.commit()

    # test 200
    book_url = url_for('api.book_by_id', book_id=book.id)
    rep = client.get(book_url)
    assert rep.status_code == 200

    data = rep.get_json()["book"]
    assert data["title"] == book.title
    assert data["isbn"] == book.isbn
    assert data["page_count"] == book.page_count


def test_put_user(client, db, book):
    # test 404
    book_url = url_for('api.book_by_id', book_id="10000")
    rep = client.put(book_url)
    assert rep.status_code == 404

    db.session.add(book)
    db.session.commit()

    data = {"title": "new_title"}

    book_url = url_for('api.book_by_id', book_id=book.id)
    # test update book
    rep = client.put(book_url, json=data)
    assert rep.status_code == 200

    data = rep.get_json()["book"]
    assert data["title"] == "new_title"

    db.session.refresh(book)

def test_delete_book(client, db, book):
    # test 404
    book_url = url_for('api.book_by_id', book_id="10000")
    rep = client.delete(book_url)
    assert rep.status_code == 404

    db.session.add(book)
    db.session.commit()

    # test get_book
    book_url = url_for('api.book_by_id', book_id=book.id)
    rep = client.delete(book_url)
    assert rep.status_code == 200
    assert db.session.query(Book).filter_by(id=book.id).first() is None


def test_create_book(client, db):
    # test bad data
    books_url = url_for('api.books')
    data = {"page_count": "100"}
    rep = client.post(books_url, json=data)
    assert rep.status_code == 400

    # test create user
    data = {"title": "new_title", "isbn": "123456789", "page_count": "100", "description": "new description", "author_first_name": "new_first_name", "author_last_name": "new_last_name"}
    rep = client.post(books_url, json=data)
    assert rep.status_code == 201

    data = rep.get_json()
    book = db.session.query(Book).filter_by(id=data["book"]["id"]).first()

    assert book.title == "new_title"
    assert book.isbn == "123456789"


def test_get_all_books(client, db, book_factory):
    books_url = url_for('api.books')
    books = book_factory.create_batch(30)

    db.session.add_all(books)
    db.session.commit()

    rep = client.get(books_url)
    assert rep.status_code == 200

    results = rep.get_json()
    for book in books:
        assert any(b["id"] == book.id for b in results["results"])


def test_search_books(client, db, book_factory):
    books_url = url_for('api.books')
    books = book_factory.create_batch(30)

    db.session.add_all(books)
    db.session.commit()

    rep = client.get(books_url, query_string={"q": "new"})
    assert rep.status_code == 200

    results = rep.get_json()
    for book in books:
        assert any(b["id"] == book.id for b in results["results"])
        
        
def test_count_occurrences(client, db, book_factory):
    url = url_for('api.count_occurrences',word="help")
    rep = client.get(url)
    assert rep.status_code == 200
    assert rep.get_json()["help"] == 5