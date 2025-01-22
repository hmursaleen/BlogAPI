from faker import Faker
import requests
import random
from django.conf import settings
from pymongo import MongoClient
fake = Faker()

# Define your API URL
BASE_URL = "http://127.0.0.1:8001/api/posts/"
client = MongoClient(settings.MONGO_URI)
db = client[settings.MONGO_DB_NAME]
collection = self.db['blog_posts']
categories = ["Technology", "Health", "Finance", "Education", "Lifestyle"]
tags_pool = ["Python", "Django", "MongoDB", "API", "Database", "Indexing", "Performance", "Faker"]


def create_post(title, content, category, tags):
    payload = {
        "title": title,
        "content": content,
        "category": category, 
        "tags": tags         
    }
    response = requests.post(BASE_URL, json=payload)
    if response.status_code == 201:
        print(f"Created post: {title}")
    else:
        print(f"Error: {response.text}")


for _ in range(1000): 
    title = fake.sentence()
    content = fake.paragraph()
    category = random.choice(categories)
    tags = random.sample(tags_pool, k=random.randint(1, 5))
    create_post(title, content, category, tags)
