from BookStore.extensions import db


class Book(db.Model):
    """Basic book model"""

    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    author_last_name = db.Column(db.String(255), nullable=False)
    author_first_name = db.Column(db.String(255), nullable=False)
    page_count = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    
    def __repr__(self):
        return '<Book %r>' % self.title
 