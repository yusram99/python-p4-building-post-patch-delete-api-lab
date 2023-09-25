#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate
from sqlalchemy.orm import Session
from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'

@app.route('/bakeries')
def bakeries():

    bakeries = Bakery.query.all()
    bakeries_serialized = [bakery.to_dict() for bakery in bakeries]

    response = make_response(
        bakeries_serialized,
        200
    )
    return response

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):

    bakery = Bakery.query.filter_by(id=id).first()
    bakery_serialized = bakery.to_dict()

    response = make_response(
        bakery_serialized,
        200
    )
    return response

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods_by_price = BakedGood.query.order_by(BakedGood.price).all()
    baked_goods_by_price_serialized = [
        bg.to_dict() for bg in baked_goods_by_price
    ]
    
    response = make_response(
        baked_goods_by_price_serialized,
        200
    )
    return response

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first()
    most_expensive_serialized = most_expensive.to_dict()

    response = make_response(
        most_expensive_serialized,
        200
    )
    return response

# Get and Post using json data
# @app.route('/baked_goods', methods=['GET', 'POST'])
# def baked_goods():
#     if request.method == 'GET':
#         baked_goods = []
#         for good in BakedGood.query.all():
#             good_dict = good.to_dict()
#             baked_goods.append(good_dict)

#         response = make_response(
#             jsonify(baked_goods),
#             200
#         )

#         return response

#     if request.method == 'POST':
#         data = request.get_json()
#         if 'name' not in data or 'price' not in data:
#             return jsonify({'error': 'Missing required fields'}), 400

#         new_baked_good = BakedGood(name=data['name'], price=data['price'])

#         try:
#             db.session.add(new_baked_good)
#             db.session.commit()
#             return jsonify({'message': 'Baked good created successfully'}), 201  # 201 Created
#         except Exception as e:
#             db.session.rollback()
#             return jsonify({'error': 'An error occurred while creating the baked good'}), 500  # 500 Internal Server Error


# getting data or putting data as form data
@app.route('/baked_goods', methods=['GET', 'POST'])
def baked_goods():
    if request.method == 'GET':
        baked_goods = []
        for good in BakedGood.query.all():
            good_dict = good.to_dict()
            baked_goods.append(good_dict)

        response = make_response(
            jsonify(baked_goods),
            200
        )

        return response

    if request.method == 'POST':
        name = request.form.get("name")
        price = request.form.get("price")

        if name is None or price is None:
            return jsonify({'error': 'Missing required fields'}), 400

        new_baked_good = BakedGood(name=name, price=price)

        try:
            db.session.add(new_baked_good)
            db.session.commit()
            return jsonify({'message': 'Baked good created successfully'}), 201  # 201 Created
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'An error occurred while creating the baked good'}), 500  # 500 Internal Server Error


@app.route('/bakeries/<int:id>', methods=['GET', 'PATCH'])
def bakeries_by_id(id):
    bakery = Bakery.query.filter(Bakery.id == id).first()
    
    if bakery == None:
        response_body = {
            "message": "This record does not exist in our database. Please try again."
        }
        response = make_response(response_body, 404)

        return response
        
    else:
        if request.method == 'GET':
            bakery_dict = bakery.to_dict()

            response = make_response(
                bakery_dict,
                200
            )

            return response

        elif request.method == 'PATCH':
            for attr in request.form:
                setattr(bakery, attr, request.form.get(attr))

            db.session.add(bakery)
            db.session.commit()

            bakery_dict = bakery.to_dict()

            response = make_response(
                bakery_dict,
                200
            )

            return response



# @app.route('/baked_goods/<int:id>', methods=['DELETE'])
# def delete_baked_goods(id):
#     baked_good = BakedGood.query.get(id)
#     if baked_good:
#         db.session.delete(baked_good)
#         db.session.commit()
#         return '', 204
#     else:
#         return jsonify({'error': 'Baked good not found'}), 404
@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_goods(id):
    session = db.session
    baked_good = session.get(BakedGood, id)

    if baked_good:
        session.delete(baked_good)
        session.commit()
        # return '', 204
        return jsonify({'message': 'Baked good deleted successfully'}), 200
    else:
        return jsonify({'error': 'Baked good not found'}), 404
    
if __name__ == '__main__':
    app.run(port=5556, debug=True)
