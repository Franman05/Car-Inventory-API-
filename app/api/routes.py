from flask import Blueprint, request, jsonify
from helpers import token_required
from models import User, Car, car_schema, cars_schema, db

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return { 'yoo': 'wee'}

api.route('/cars', methods = ['POST'])
@token_required
def create_car(current_user_token):
    make = request.json['make']
    model = request.json['model']
    sale_price = request.json['sale_price']
    color = request.json['color']
    year = request.json['year']
    mpg = request.json['mpg']
    new_used = request.json['new_used']
    user_token = current_user_token.token

    car = Car(make,model,sale_price,color,year,mpg,new_used,user_token = user_token)

    db.session.add(car)
    db.session.commit()