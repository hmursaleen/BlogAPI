from pymongo import MongoClient
from django.conf import settings
from datetime import datetime

#Check if you can import from bson.objectid import ObjectId in the beginning.

class BlogPost:
    def __init__(self):
        # Initialize the MongoDB client and database
        client = MongoClient(settings.MONGO_URI)
        self.db = client[settings.MONGO_DB_NAME]
        self.collection = self.db['blog_posts']

    def create_post(self, title, content, category, tags):
        post = {
            'title': title,
            'content': content,
            'category': category,
            'tags': tags,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
        }
        result = self.collection.insert_one(post)
        return result.inserted_id

    def get_post(self, post_id):
        from bson.objectid import ObjectId
        return self.collection.find_one({'_id': ObjectId(post_id)})

    def update_post(self, post_id, updates):
        from bson.objectid import ObjectId
        updates['updated_at'] = datetime.utcnow()
        result = self.collection.update_one(
            {'_id': ObjectId(post_id)}, {'$set': updates}
        )
        return result.modified_count

    def delete_post(self, post_id):
        from bson.objectid import ObjectId
        result = self.collection.delete_one({'_id': ObjectId(post_id)})
        return result.deleted_count
