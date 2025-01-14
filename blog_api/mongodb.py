from typing import Optional
from pymongo import MongoClient
from pymongo.database import Database
import os
from dotenv import load_dotenv
import logging

'''
Since PyMongo is not an ORM, you cannot use Django's DATABASES setting for MongoDB. Instead, 
you'll establish a connection manually.
'''
# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MongoDB:
    _instance = None
    _client: Optional[MongoClient] = None
    _db: Optional[Database] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._client is None:
            self._connect()

    def _connect(self):
        """Establish MongoDB connection"""
        try:
            host = os.getenv('MONGODB_HOST', 'localhost')
            port = int(os.getenv('MONGODB_PORT', '27017'))
            database = os.getenv('MONGODB_DATABASE', 'blog_db')

            # Create MongoDB connection URI
            uri = f"mongodb://{host}:{port}"

            # Create client and connect to database
            self._client = MongoClient(uri)
            self._db = self._client[database]

            # Test connection
            self._client.admin.command('ping')
            logger.info("Successfully connected to MongoDB")

        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {str(e)}")
            raise

    @property
    def client(self) -> MongoClient:
        """Get MongoDB client instance"""
        return self._client

    @property
    def db(self) -> Database:
        """Get database instance"""
        return self._db

    def close(self):
        """Close MongoDB connection"""
        if self._client:
            self._client.close()
            self._client = None
            self._db = None
            logger.info("MongoDB connection closed")

# Create global instance
mongodb = MongoDB()

try:
    # Test the connection
    mongodb.client.admin.command('ping')
    print("Successfully connected to MongoDB!")
    
    # Create a test collection and insert a document
    collection = mongodb.db.test_collection
    result = collection.insert_one({"test": "Hello MongoDB"})
    print("Inserted document ID:", result.inserted_id)
    
    # Retrieve the document
    doc = collection.find_one({"test": "Hello MongoDB"})
    print("Retrieved document:", doc)
    
    # List all collections
    print("\nCollections in database:")
    print(mongodb.db.list_collection_names())
    
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    mongodb.close()