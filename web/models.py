import datetime
from peewee import *

db = SqliteDatabase('products.db')

class Product(Model):
    class Meta:
        database = db

    name = CharField()
    upc = CharField(unique=True)
    url = CharField()
    add_to_cart_url = CharField()
    created = DateTimeField(default=datetime.datetime.now)
    empty = BooleanField()
    reordered = BooleanField()
    size = CharField()

    def get_parsed_weight(self):
        parsed = int(self.size.replace(' oz', ''))
        return parsed

    def to_dict(self):
        return {
            'name': self.name,
            'upc': self.upc,
            'url': self.url,
            'add_to_cart_url': self.add_to_cart_url,
            'created': self.created,
            'empty': self.empty,
            'reordered': self.reordered,
            'size': self.size,
            'weight': self.get_parsed_weight(),
            'history': [h.to_dict() for h in self.history.order_by(ProductHistory.timestamp.asc())]
        }


class ProductHistory(Model):
    class Meta:
        database = db
    
    product = ForeignKeyField(Product, backref='history')
    weight = FloatField()
    timestamp = DateTimeField(default=datetime.datetime.now)

    def to_dict(self):
        return {
            'weight': self.weight,
            'timestamp': self.timestamp
        }