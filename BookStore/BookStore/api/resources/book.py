from flask import request
from flask_restful import Resource
from BookStore.api.schemas import BookSchema
from BookStore.models import Book
from BookStore.extensions import db
from BookStore.commons.pagination import paginate
import requests,json

class BookResource(Resource):
    """Single object resource

    ---
    get:
      tags:
        - api
      summary: Get a book
      description: Get a single book by ID
      parameters:
        - in: path
          name: book_id
          schema:
            type: integer
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  book: BookSchema
        404:
          description: book does not exists
    put:
      tags:
        - api
      summary: Update a book
      description: Update a single book by ID
      parameters:
        - in: path
          name: book_id
          schema:
            type: integer
      requestBody:
        content:
          application/json:
            schema:
              BookSchema
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: book updated
                  book: BookSchema
        404:
          description: book does not exists
    delete:
      tags:
        - api
      summary: Delete a book
      description: Delete a single book by ID
      parameters:
        - in: path
          name: book_id
          schema:
            type: integer
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: book deleted
        404:
          description: book does not exists
    """

    def get(self, book_id:int) -> dict:
      """
      Get a single book
      
      :param book_id: The ID of the book
      """
      schema = BookSchema()
      book = Book.query.get_or_404(book_id)
      return {"book": schema.dump(book)}

    def put(self, book_id:int) -> dict:
      """
      Update a book
      
      :param book_id: The ID of the book
      """
      schema = BookSchema(partial=True)
      book = Book.query.get_or_404(book_id)
      book = schema.load(request.json, instance=book)

      db.session.commit()

      return {"msg": "book updated", "book": schema.dump(book)}

    def delete(self, book_id:int) -> dict:
      """
      Delete a book
      
      :param book_id: The ID of the book
      """
      book = Book.query.get_or_404(book_id)
      db.session.delete(book)
      db.session.commit()

      return {"msg": "book deleted"}


class BookList(Resource):
    """Creation and get_all

    ---
    get:
      tags:
        - api
      summary: Get a list of books
      description: Get a list of paginated books
      responses:
        200:
          content:
            application/json:
              schema:
                allOf:
                  - $ref: '#/components/schemas/PaginatedResult'
                  - type: object
                    properties:
                      results:
                        type: array
                        items:
                          $ref: '#/components/schemas/BookSchema'
    post:
      tags:
        - api
      summary: Create a book
      description: Create a new book
      requestBody:
        content:
          application/json:
            schema:
              BookSchema
      responses:
        201:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: book created
                  book: BookSchema
    """
    def get(self) -> dict:
      """
      Get all books
      """
      query = Book.query
      schema = BookSchema(many=True)
      return paginate(query, schema)

    def post(self) -> dict:
      """
      Create a book
      """
      schema = BookSchema()
      book = schema.load(request.json)

      db.session.add(book)
      db.session.commit()

      return {"msg": "book created", "book": schema.dump(book)}, 201

class Search(Resource):
    """Search

    ---
    get:
      tags:
        - api
      summary: Search for books
      description: Search for books
      parameters:
        - in: query
          name: q
          schema:
            type: string
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  books:
                    type: array
                    items:
                      $ref: '#/components/schemas/BookSchema'
    """
    def get(self) -> dict:
      """
      Search for books
      """
      query_string = request.args.get("q")
      query = Book.query.filter(Book.title.contains(query_string) | Book.description.contains(query_string) | Book.isbn.contains(query_string) | Book.author_first_name.contains(query_string) | Book.author_last_name.contains(query_string) | Book.page_count.contains(query_string))
      schema = BookSchema(many=True)
      return {"books": schema.dump(query)}

class getCountOccurrences(Resource):
  """
  Get the number of occurrences of a word in a book
  ---
  get:
      tags:
        - api
      summary: Get a count of occurrences of a word in a book
      description: Get a count of occurrences of a word in a book
      parameters:
        - in: path
          name: word
          schema:
            type: string
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  count:
                    type: integer
                    example: 3
  """
  def get(self,word:str) -> dict:
    """
    Get the number of occurrences of a word in a book
    
    :param word: The word to search for
    """
    url = "http://api2:5000/api/v2/count_occurrences/"+word
    response = requests.get(url,verify=False)
    return json.loads(response.text)