from flask import Blueprint, request, jsonify
from helpers import token_required
from models import User, Car, car_schema, cars_schema, db

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return { 'yoo': 'wee'}

@api.route('/cars', methods = ['POST'])
@token_required
def create_car(current_user_token):
    make = request.json['make']
    model = request.json['model']
    sale_price = request.json['sale_price']
    color = request.json['color']
    year = request.json['year']
    new_used = request.json['new_used']
    user_token = current_user_token.token

    car = Car(make,model,sale_price,color,year,new_used,user_token = user_token)

    db.session.add(car)
    db.session.commit()

    response = car_schema.dump(car)
    return jsonify(response)

@api.route('/cars', methods = ['GET'])
@token_required
def get_cars(current_user_token):
    owner = current_user_token.token
    cars = Car.query.filter_by(user_token = owner).all()
    response = cars_schema.dump(cars)
    return jsonify(response)

@api.route('/cars/<id>', methods = ['GET'])
@token_required
def get_car(current_user_token, id):
    car = Car.query.get(id)
    response = car_schema.dump(car)
    return jsonify(response)
    
# Update endpoint
@api.route('/cars/<id>', methods = ['POST', 'PUT'])
@token_required
def update_car(current_user_token, id):
    car = Car.query.get(id) 
    car.make = request.json['make']
    car.model = request.json['model']
    car.sale_price = request.json['sale_price']
    car.color = request.json['color']
    car.year = request.json['year']
    car.new_used = request.json['new_used']
    car.user_token = current_user_token.token

    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)

@api.route('/cars/<id>', methods = ['DELETE'])
@token_required
def delete_car(current_user_token, id):
    car = Car.query.get(id)
    db.session.delete(car)
    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)