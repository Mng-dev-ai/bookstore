import factory
from BookStore.models import Book


class BookFactory(factory.Factory):

    class Meta:
        model = Book

    isbn = "test"
    title = "test"
    author_first_name = "test"
    author_last_name = "test"
    description = "test"
    page_count = 1
