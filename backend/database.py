from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

# Connect to the MongoDB database using the provided connection string
client = MongoClient(os.getenv("DATABASE_CONNECT"))

db = client.rag_db

# Define a MongoDB collection for storing chats
chat_collection = db.chat_collection