from flask import Flask, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# Replace with your actual MongoDB connection string
client = MongoClient("mongodb+srv://weddingverse:annihilation@sachan.6fapy.mongodb.net/")
db = client["weddingverse"]
collection = db["venues"]

@app.route('/venues', methods=['GET'])
def get_venues():
    venues = collection.find().limit(10)
    venues_list = []
    for venue in venues:
        venue['_id'] = str(venue['_id'])
        venues_list.append(venue)
    return jsonify(venues_list)

if __name__ == '__main__':
    app.run(debug=True)
