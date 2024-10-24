from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson.objectid import ObjectId
import jwt
import datetime
import bcrypt
import uuid

app = Flask(__name__)

# Replace with your actual MongoDB connection strings
client = MongoClient("mongodb+srv://sachanakshat:annihilation@sachan.6fapy.mongodb.net/")
db_weddingverse = client["weddingverse"]
collection_venues = db_weddingverse["venues"]
db_weddingusers = client["weddingusers"]
collection_users = db_weddingusers["users"]

JWT_SECRET = "weddingverse"  # Replace with a strong, randomly generated secret key

active_sessions = {}

@app.route('/venues', methods=['GET'])
def get_venues():
    token = request.headers.get('Authorization')
    session_id = request.headers.get('Session-ID')

    if not token:
        return jsonify({"message": "Token is missing"}), 401

    try:
        data = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        username = data["user"]
        if session_id in active_sessions and active_sessions[session_id] == username:
            venues = collection_venues.find().limit(10)
            venues_list = []
            for venue in venues:
                venue['_id'] = str(venue['_id'])
                venues_list.append(venue)
            return jsonify(venues_list)
        else:
            return jsonify({"message": "Unauthorized access"}), 401
    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"message": "Invalid token"}), 401
    except Exception as e:
        return jsonify({"message": str(e)}), 500

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
    if username in active_sessions.values():
        return jsonify({"message": "User already logged in"}), 401
    token = jwt.encode({"user": username, "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, JWT_SECRET)
    session_id = str(uuid.uuid4())
    active_sessions[session_id] = username
    return jsonify({"token": token, "session_id": session_id})

@app.route('/logout', methods=['POST'])
def logout():
    session_id = request.headers.get('Session-ID')
    if session_id in active_sessions:
        del active_sessions[session_id]
        return jsonify({"message": "Logged out successfully"})
    else:
        return jsonify({"message": "Not logged in"}), 401

if __name__ == '__main__':
    app.run(debug=True)
