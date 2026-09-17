from flask import Flask, jsonify, request, session
from flask_pymongo import PyMongo
import bcrypt
import jwt
from flask_jwt_extended import JWTManager, create_access_token
from flask_cors import CORS, cross_origin
import os
from dotenv import load_dotenv

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

@app.route("/adminRegister", methods=['POST'])
def adminRegister():
    allusers = mongo.db.admins

    user = allusers.find_one({'email':request.json['email']})
    companyName = allusers.find_one({'companyName':request.json['companyName']})
    phone = allusers.find_one({'phone':request.json['phone']})

    if user:
        return jsonify(message='Email already exits'), 401
    if companyName:
        return jsonify(message='companyName already exists'), 401
    
    if phone:
        return jsonify(message='Phone Number already exists'), 401
    
    if request.json['password'] != request.json['cpassword']:
        return jsonify(message='Password not Matching!!!'), 401
    
    hashpw = bcrypt.hashpw(

        request.json['password'].encode('utf-8'),bcrypt.gensalt()

    )

    hashcpw = bcrypt.hashpw(
    
        request.json['password'].encode('utf-8'), bcrypt.gensalt()
    )

    access_token = create_access_token(identity=request.json['email'])
    

    allusers.insert_one({
        'email': request.json['email'],
        'companyName': request.json['companyName'],
        'phone': request.json['phone'],
        'password': str(hashpw),
        'cpassword': str(hashcpw),
        'tokens': [
            {
                'token': str(access_token)
            }
        ]
    })

    return jsonify(token= str(access_token)), 201

@app.route("/adminLogin", methods=['POST'])
def adminLogin():
    allusers = mongo.db['admins']
    user = allusers.find_one({'email': request.json['email']})

    if user:
        password_bytes = request.json['password'].encode('utf-8')
        stored_hash = user['password']

        # Strip any "b'...' " wrapper if saved as a stringified byte object
        if isinstance(stored_hash, str) and stored_hash.startswith("b'") and stored_hash.endswith("'"):
            stored_hash = stored_hash[2:-1]
            
        stored_hash_bytes = stored_hash.encode('utf-8') if isinstance(stored_hash, str) else stored_hash

        # Verify password correctly
        if bcrypt.checkpw(password_bytes, stored_hash_bytes):
            access_token = create_access_token(identity=request.json['email'])
            
            # Modern update method instead of deleted .save()
            allusers.update_one(
                {'_id': user['_id']},
                {'$push': {'tokens': {'token': str(access_token)}}}
            )
            return jsonify(token=str(access_token)), 201

    return jsonify(message='Invalid userid/password'), 401
        
@app.route("/logoutAdmin", methods=['POST'])
def logoutAdmin():
    allusers = mongo.db.admins
    user = allusers.find_one({'tokens.token':request.json['auth']})
    if user:
        # Use update_one + $set to clear tokens instead of legacy .save()
        allusers.update_one(
            {'_id': user['_id']},
            {'$set': {'tokens': []}}
        )
        return jsonify(message='Logout Successful'), 201

    return jsonify(message='Logout Failed'), 401
    

if __name__=='__main__':
    app.run(debug=True, port=5001)


