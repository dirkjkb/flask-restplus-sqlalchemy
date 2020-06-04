from . import db


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.String(), primary_key=True)
    name = db.Column(db.String())
    size = db.Column(db.Integer)
    description = db.Column(db.String(), nullable=True)

    def __init__(self, id: str, name: str, size: int, description: str = None):
        self.id = id
        self.name = name
        self.size = size
        self.description = description

    def __repr__(self):
        return '<id {}>'.format(self.id)
