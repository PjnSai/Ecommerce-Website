from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
import bcrypt

from flask_jwt_extended import JWTManager, create_access_token
from flask_cors import CORS
import os
from dotenv import load_dotenv
from bson.objectid import ObjectId

# Load variables from .env
load_dotenv()

app = Flask(__name__)
CORS(app)

app.config["MONGO_URI"] = os.getenv("MONGO_URI")
app.secret_key = os.getenv("SECRET_KEY")
app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")

print("Loaded MONGO_URI:", app.config["MONGO_URI"])

mongo = PyMongo(app)
jwt = JWTManager(app)


@app.route("/")
def hello_world():
    return 'Hello World'

# ---------------------------------------------------------
# AUTH ROUTES
# ---------------------------------------------------------

@app.route("/adminRegister", methods=['POST'])
def adminRegister():
    allusers = mongo.db.admins

    user = allusers.find_one({'email': request.json.get('email')})
    companyName = allusers.find_one({'companyName': request.json.get('companyName')})
    phone = allusers.find_one({'phone': request.json.get('phone')})

    if user:
        return jsonify(message='Email already exists'), 401
    if companyName:
        return jsonify(message='Company name already exists'), 401
    if phone:
        return jsonify(message='Phone number already exists'), 401
    
    if request.json.get('password') != request.json.get('cpassword'):
        return jsonify(message='Passwords do not match!'), 401
    
    hashpw = bcrypt.hashpw(request.json['password'].encode('utf-8'), bcrypt.gensalt())
    hashcpw = bcrypt.hashpw(request.json['password'].encode('utf-8'), bcrypt.gensalt())

    access_token = create_access_token(identity=request.json['email'])

    allusers.insert_one({
        'email': request.json['email'],
        'companyName': request.json['companyName'],
        'phone': request.json['phone'],
        'password': str(hashpw),
        'cpassword': str(hashcpw),
        'tokens': [{'token': str(access_token)}],
        'products': []
    })

    return jsonify(token=str(access_token)), 201


@app.route("/adminLogin", methods=['POST'])
def adminLogin():
    allusers = mongo.db.admins
    user = allusers.find_one({'email': request.json.get('email')})

    if user:
        password_bytes = request.json.get('password', '').encode('utf-8')
        stored_hash = user['password']

        if isinstance(stored_hash, str) and stored_hash.startswith("b'") and stored_hash.endswith("'"):
            stored_hash = stored_hash[2:-1]
            
        stored_hash_bytes = stored_hash.encode('utf-8') if isinstance(stored_hash, str) else stored_hash

        if bcrypt.checkpw(password_bytes, stored_hash_bytes):
            access_token = create_access_token(identity=request.json['email'])
            
            allusers.update_one(
                {'_id': user['_id']},
                {'$push': {'tokens': {'token': str(access_token)}}}
            )
            return jsonify(token=str(access_token)), 201

    return jsonify(message='Invalid userid/password'), 401

        
@app.route("/logoutAdmin", methods=['POST'])
def logoutAdmin():
    allusers = mongo.db.admins
    user = allusers.find_one({'tokens.token': request.json.get('auth')})
    if user:
        allusers.update_one(
            {'_id': user['_id']},
            {'$set': {'tokens': []}}
        )
        return jsonify(message='Logout Successful'), 201

    return jsonify(message='Logout Failed'), 401


# ---------------------------------------------------------
# PRODUCT & ADMIN DATA ROUTES
# ---------------------------------------------------------

@app.route("/getAdminData", methods=['POST'])
def getAdminData():
    allusers = mongo.db.admins
    token = request.json.get('auth')
    
    user = allusers.find_one({'tokens.token': token})
    if user:
        user['_id'] = str(user['_id'])
        return jsonify(user), 200

    return jsonify(message="Admin not found for given token"), 400


@app.route("/addProduct", methods=['POST'])
def addProduct():
    allusers = mongo.db.admins
    data = request.json
    auth_token = data.get('auth')

    user = allusers.find_one({'tokens.token': auth_token})
    if not user:
        return jsonify(message="Unauthorized token"), 401

    raw_price = str(data.get('productPrice', ''))
    if '<=>' in raw_price:
        price, prod_type = raw_price.split('<=>')
    else:
        price = raw_price
        prod_type = "unit"

    new_product = {
        '_id': str(ObjectId()),
        'productName': data.get('productName'),
        'productPrice': price,
        'productType': prod_type,
        'productUrl': data.get('productUrl')
    }

    allusers.update_one(
        {'_id': user['_id']},
        {'$push': {'products': new_product}}
    )

    return jsonify(message="Product added successfully"), 201


@app.route("/editProduct", methods=['PUT'])
def editProduct():
    allusers = mongo.db.admins
    data = request.json
    uid = data.get('uid')
    
    if not uid:
        return jsonify(message="Missing uid"), 400

    try:
        raw_price = str(data.get('productPrice', ''))
        if '<=>' in raw_price:
            price, prod_type = raw_price.split('<=>')
        else:
            price = raw_price
            prod_type = "unit"

        updated_product = {
            '_id': str(ObjectId()),
            'productName': data.get('productName'),
            'productPrice': price,
            'productType': prod_type,
            'productUrl': data.get('productUrl')
        }

        allusers.update_one(
            {'_id': ObjectId(uid)},
            {'$set': {'products.$[elem]': updated_product}},
            array_filters=[{'elem.productName': data.get('productName')}]
        )

        return jsonify(message="Product updated successfully"), 201
    except Exception as e:
        return jsonify(message=str(e)), 500


@app.route("/deleteProduct", methods=['PUT', 'DELETE'])
def deleteProduct():
    allusers = mongo.db.admins
    uid = request.json.get('uid')

    if not uid:
        return jsonify(message="Missing uid"), 400

    try:
        allusers.update_one(
            {'_id': ObjectId(uid)},
            {'$pull': {'products': {'_id': uid}}}
        )
        return jsonify(message="Product deleted successfully"), 201
    except Exception as e:
        return jsonify(message=str(e)), 500


if __name__ == '__main__':
    app.run(debug=True, port=5001)