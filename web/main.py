import controller
from flask import Flask, jsonify, request
from models import db, Product, ProductHistory

app = Flask(__name__)

db.connect()
db.drop_tables([Product, ProductHistory])
db.create_tables([Product, ProductHistory])

@app.route('/')
def hello():
    return jsonify({
        'hello': 'world'
    })


@app.route('/products/')
def products():
    products = Product.select()
    return jsonify({
        'products': [p.to_dict() for p in products],
        'count': products.count()
    })


@app.route('/products/<string:upc>/', methods=['GET'])
def product(upc):
    product = controller.get_product(upc)

    if product:
        return jsonify(product.to_dict())
    
    return jsonify({'error': 'product not found'})


@app.route('/update/<string:upc>/', methods=['POST'])
def update(upc):
    weight = request.form['weight'] if 'weight' in request.form else None
    empty = request.form['empty'] if 'empty' in request.form else None
    reordered = request.form['reordered'] if 'reordered' in request.form else None
    product = controller.get_product(upc)

    if product:
        if weight and not product.empty:
            history = ProductHistory(
                product = product,
                weight = weight
            )
            history.save()

        if empty:
            product.empty = True
            product.save()

        if reordered:
            product.reordered = True
            product.save()

        return jsonify(product.to_dict())
    
    return jsonify({'error': 'product not found'})