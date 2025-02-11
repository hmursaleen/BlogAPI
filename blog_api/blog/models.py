from pymongo import MongoClient, ASCENDING, DESCENDING
from django.conf import settings
from datetime import datetime
from bson.objectid import ObjectId


class BlogPost:
    def __init__(self):
        # Initialize the MongoDB client and database
        client = MongoClient(settings.MONGO_URI)
        self.db = client[settings.MONGO_DB_NAME]
        self.collection = self.db['blog_posts']
        self._create_indexes()

    
    def _create_indexes(self):
        indexes = [
            ("id", ASCENDING),
            ("title", ASCENDING),
            ("created_at", DESCENDING),
            ("category", ASCENDING),
            ("tags", ASCENDING),
        ]

        for index in indexes:
            self.collection.create_index(index)


    def create(self, data):
        data['created_at'] = datetime.utcnow()
        data['updated_at'] = datetime.utcnow()
        result = self.collection.insert_one(data)
        return result.inserted_id


    def get(self, post_id):
        return self.collection.find_one({'_id': ObjectId(post_id)})

    def update(self, post_id, data):
        data['updated_at'] = datetime.utcnow()
        result = self.collection.update_one(
            {'_id': ObjectId(post_id)}, {'$set': data}
        )
        return result.modified_count

    def delete(self, post_id):
        result = self.collection.delete_one({'_id': ObjectId(post_id)})
        return result.deleted_count

    def search(self, filters):
        return self.collection.find(filters)



'''
Monitoring and Logs:

Use monitoring tools like Prometheus or Grafana to observe system resource usage (CPU, memory, etc.).
Analyze logs to detect issues during high load.
Caching:

Use Redis or a similar caching layer to reduce database load for frequently accessed data.
Database Optimization:

Ensure indexes are set up properly for MongoDB queries.
Use connection pooling for efficient database interactions.
'''