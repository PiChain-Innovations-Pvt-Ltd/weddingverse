from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson.objectid import ObjectId
import jwt
import datetime
import bcrypt

app = Flask(__name__)

# Replace with your actual MongoDB connection strings
client = MongoClient("mongodb+srv://sachanakshat:annihilation@sachan.6fapy.mongodb.net/")
db_weddingverse = client["weddingverse"]
collection_venues = db_weddingverse["venues"]
db_weddingusers = client["weddingusers"]
collection_users = db_weddingusers["users"]

JWT_SECRET = "weddingverse"  # Replace with a strong, randomly generated secret key

@app.route('/venues', methods=['GET'])
def get_venues():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"message": "Token is missing"}), 401
    try:
        data = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        venues = collection_venues.find().limit(10)
        venues_list = []
        for venue in venues:
            venue['_id'] = str(venue['_id'])
            venues_list.append(venue)
        return jsonify(venues_list)
    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"message": "Invalid token"}), 401

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    collection_users.insert_one({"username": username, "password": hashed_password})
    return jsonify({"message": "User registered successfully"})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400
    user = collection_users.find_one({"username": username})
    if not user:
        return jsonify({"message": "User not found"}), 401
    if not bcrypt.checkpw(password.encode('utf-8'), user['password']):
        return jsonify({"message": "Incorrect password"}), 401
    token = jwt.encode({"user": username, "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, JWT_SECRET)
    return jsonify({"token": token})

if __name__ == '__main__':
    app.run(debug=True)
