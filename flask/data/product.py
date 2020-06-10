from typing import List
from . import db


class ProductModel(db.Model):
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


class Product(object):

    def add(self, product_id: str, name: str, size: int, description: str) -> None:
        product = ProductModel(id=product_id, name=name, size=size, description=description)
        db.session.add(product)
        db.session.commit()

    def get(self, product_id: str) -> ProductModel:
        return ProductModel.query.filter_by(id=product_id).first()

    def all(self) -> List[ProductModel]:
        return ProductModel.query.all()
