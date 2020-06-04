import logging
import uuid

from flask_restplus import Resource, Namespace, fields, abort
from data.product import Product as db_product
from data.product import db

_logger = logging.getLogger()
api = Namespace('product', description='All The products we have')

add_product = api.model('AddProduct', {
    'name': fields.String(required=True, description='The Name of the Product'),
    'size': fields.Integer(required=True, description='Size of the object in meter'),
    'description': fields.String(required=False, description='description of the product', default=None)
})

full_product = api.clone('Product', add_product, {
    'id': fields.String(required=True, description='unique product id.')
})


@api.route('')
class AddProduct(Resource):
    
    @api.expect(add_product)
    def post(self) -> full_product:
        new_product = api.payload
        new_product['id'] = str(uuid.uuid4())
        product = db_product(id=new_product['id'], name=new_product['name'], size=new_product['size'], description=new_product['description'])
        db.session.add(product)
        db.session.commit()
        return new_product


@api.route('/<id>')
class GetProduct(Resource):
    
    @api.marshal_with(full_product)
    def get(self, id: str = None) -> full_product:
        product = db_product.query.filter_by(id=id).first()
        if product is None:
            abort(404, custom='Item does not exist')
        else:
            return product


@api.route('/list')
class ListProducts(Resource):

    @api.marshal_list_with(full_product)
    def get(self) -> []:
        return db_product.query.all()
