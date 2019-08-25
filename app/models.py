from app import db
from flask import url_for
from app.error import ValidationError
from datetime import datetime
from dateutil import parser as datetime_parser
from dateutil.tz import tzutc
from app.utils import split_url


class Customer(db.Model):

    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    orders = db.relationship('Order', backref='customer', lazy='dynamic')


    def get_url(self):
        return url_for('get_customer', id=self.id, _external=True)

    def export_data(self):
        return {
            'self_url': self.get_url(),
            'name': self.name,
            'orders_url': url_for('get_customer_orders', _external=True, id=self.id)
        }

    def import_data(self, data):
        try:
            self.name = data['name']
        except KeyError as e:
            raise ValidationError('Invalid customer: missing ' + e.args[0])
        return self

class Product(db.Model):

    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    items = db.relationship("Item", backref='product', lazy='dynamic')

    def get_product(self):
        return url_for('get_product', id.self.id, _external=True)

    def export_data(self):
        return {
            'name': self.name,
            'self_url': self.get_product()
        }

    def import_data(self, data):
        try:
            self.name = data['name']
        except KeyError as e:
            raise ValidationError('Invalid customer: missing ' + e.args[0])
        return self


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), index=True)
    date = db.Column(db.DateTime, default=datetime.now)
    items = db.relationship('Item', backref='order', lazy='dynamic',
                            cascade='all, delete-orphan')

    def get_order(self):
        return url_for('get_order', id=self.id, _external=True)

    def export_data(self):
        return {
            'name': self.name,
            'self_url': self.get_order(),
            'customer_url': self.customer.get_url(),
            'date': self.date.isoformat() + 'Z',
            'items_url': url_for('get_order_items', id=self.id, _external=True)
        }

    def import_data(self, data):
        try:
            self.date = datetime_parser.parse(data['date']).astimezone(
                tzutc()).replace(tzinfo=None)
        except KeyError as e:
            raise ValidationError('Invalid order: missing ' + e.args[0])
        return self


class Item(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), index=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), index=True)
    quantity = db.Column(db.Integer)

    def get_item(self):
        return url_for('get_item', _external=True, id=self.id)

    def export_data(self):
        return {
            'self_url': self.get_item(),
            'product_url': self.product.get_product(),
            'order_url': self.order.get_order(),
            'quantity': self.quantity
        }

    def import_data(self, data):
        try:
            endpoint, args = split_url(data['product_url'])
            self.quantity = int(data['quantity'])
        except KeyError as e:
            raise ValidationError('Invalid order: missing ' + e.args[0])
        if endpoint != 'get_product' or not 'id' in args:
            raise ValidationError('Invalid product URL: ' +
                                  data['product_url'])
        self.product = Product.query.get(args['id'])
        if self.product is None:
            raise ValidationError('Invalid product URL: ' +
                                  data['product_url'])
        return self








