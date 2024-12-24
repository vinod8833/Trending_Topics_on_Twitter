from pymongo import MongoClient
import os

def get_db_connection():
    client = MongoClient(os.getenv("MONGO_URI"))
    db = client["stir_tech"]
    return db

def insert_to_db(data):
    db = get_db_connection()
    collection = db["trending_topics"]
    collection.insert_one(data)
