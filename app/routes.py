from app import app
from app import db, auth
from flask import jsonify, request, g
from app.models import Customer, Product, Item, Order, User

@auth.verify_password
def verify_password(username, password):
    g.user = User.query.filter_by(username=username).first()
    if g.user is None:
        return False
    return g.user.verify_password(password)

@app.before_request
@auth.login_required
def before_request():
    pass

@auth.error_handler
def unauthorized():
    response = jsonify({'status': 401, 'error': 'unauthorized',
                        'message': 'please authenticate'})
    response.status_code = 401
    return response


@app.route('/customers/', methods=['GET'])
def get_customers():
    return jsonify({
        'customers': [customer.get_url() for customer in Customer.query.all()]
    })


@app.route('/customers/<int:id>', methods=['GET'])
def get_customer(id):
    return jsonify(Customer.query.get_or_404(id).export_data())


@app.route('/customers/', methods=['POST'])
def new_customer():
    customer = Customer()
    customer.import_data(request.json)
    db.session.add(customer)
    db.session.commit()
    return jsonify({}), 201, {'Location': customer.get_url()}


@app.route('/customers/<int:id>/', methods=['PUT'])
def edit_customer(id):
    customer = Customer.query.get_or_404(id)
    customer.import_data(request.json)
    db.session.add(customer)
    db.session.commit()
    return jsonify({}), 204


@app.route("/products/", methods=["GET"])
def get_products():
    return jsonify({
        'products': [product.get_url() for product in Product.query.all()]
    })


@app.route("/products/<int:id>", methods=["GET"])
def get_product(id):
    return jsonify(Product.query.get_or_404(id).export_data())


@app.route("/products/", methods=["POST"])
def new_product():
    product = Product()
    product.import_data(request.json)
    db.session.add(product)
    db.session.commit()
    return jsonify({}), 201, {'Location': product.get_url()}


@app.route("/products/<int:id>/", methods=["PUT"])
def edit_product(id):
    product = Product.query.get_or_404(id)
    product.import_data(request.json)
    db.session.add(product)
    db.session.commit()
    return jsonify({}), 204


@app.route("/orders/", methods=['GET'])
def get_orders():
    return jsonify({
        'orders': [order.get_url() for order in Order.query.all()]
    })


@app.route("/orders/<int:id>/", methods=["GET"])
def get_order(id):
    order = Order.query.get_or_404(id)
    return jsonify(order.export_data())


@app.route("/customers/<int:id>/orders/", methods=['GET'])
def get_customer_orders(id):
    customer = Customer.query.get_or_404(id)
    orders = customer.orders.all()
    return jsonify({
        'orders': [order.get_url() for order in orders]
    })


@app.route("/orders/<int:id>/", methods=['DELETE'])
def delete_order(id):
    order  = Order.query.get_or_404(id)
    db.session.delete(order)
    db.session.commit()
    return jsonify({}), 204


@app.route("/customers/<int:id>/orders/", methods=["POST"])
def new_customer_order(id):
    customer = Customer.query.get_or_404(id)
    order = Order(customer=customer)
    order.import_data(request.json)
    db.session.add(order)
    db.session.commit()
    return jsonify({}), 201, {'Location': order.get_url()}


@app.route('/orders/<int:id>/', methods=['PUT'])
def edit_order(id):
    order = Order.query.get_or_404(id)
    order.import_data(request.json)
    db.session.add(order)
    db.session.commit()
    return jsonify({}), 204

@app.route("/orders/<int:id>/items/", methods=["GET"])
def get_order_items(id):
    order = Order.query.get_or_404(id)
    return jsonify({
        "items": [item.get_url() for item in order.items.all()]
    })

@app.route("/orders/<int:id>/items/", methods=['POST'])
def new_order_item(id):
    order = Order.query.get_or_404(id)
    item = Item(order=order)
    item.import_data(request.json)
    db.session.add(item)
    db.session.commit()
    return jsonify({}), 201, {'Location': item.get_url()}

@app.route('/items/<int:id>/', methods=['GET'])
def get_item(id):
    return jsonify(Item.query.get_or_404(id).export_data())


@app.route('/items/<int:id>/', methods=['PUT'])
def edit_item(id):
    item = Item.query.get_or_404(id)
    item.import_data(request.json)
    db.session.add(item)
    db.session.commit()
    return jsonify({}), 204


@app.route('/items/<int:id>', methods=['DELETE'])
def delete_item(id):
    item = Item.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({}), 204
