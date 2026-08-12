from flask import Flask, jsonify, request, session
from flask_pymongo import PyMongo
import bcrypt
import jwt
from flask_jwt_extended import JWTManager, create_access_token
from flask_cors import CORS, cross_origin

app = Flask(__name__)
jwt = JWTManager(app)
CORS(app)

app.config['MONGO_URI'] = 'mongodb+srv://admin:MySecurePassword123@cluster0.xc8wpi0.mongodb.net/EWebsiteFlask?appName=Cluster0'
mongo = PyMongo(app)


app.secret_key = 'this-is-a-very-long-and-highly-secure-secret-key-for-session-management'
app.config['JWT_SECRET_KEY'] = 'another-super-long-secure-and-private-secret-key-for-generating-jwts'

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
        # Get password bytes and stored hash bytes
        password_bytes = request.json['password'].encode('utf-8')
        stored_hash = user['password'].encode('utf-8')

        # Use bcrypt.checkpw instead of hashpw == password
        if bcrypt.checkpw(password_bytes, stored_hash):
            access_token = create_access_token(identity=request.json['email'])
            new_token = {'token': str(access_token)}

            # Use update_one + $push instead of legacy .save()
            allusers.update_one(
                {'_id': user['_id']},
                {'$push': {'tokens': new_token}}
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


