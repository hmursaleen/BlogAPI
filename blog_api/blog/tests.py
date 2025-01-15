from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from pymongo import MongoClient
from django.conf import settings


class BlogPostSearchTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        """
        Set up the initial data for the test cases.
        This runs once for the entire test class.
        """
        cls.client = APIClient() #for testing API endpoints
        cls.mongo_client = MongoClient(settings.MONGO_URI)
        cls.db = cls.mongo_client[settings.MONGO_DB_NAME]
        cls.collection = cls.db["blog_posts"]
        cls.blog_url = "/api/posts/"

        # Insert mock data
        cls.sample_data = [
            {
                "title": "Python Programming",
                "content": "Learn Python programming with examples.",
                "category": "Programming",
                "tags": ["python", "coding"],
            },
            {
                "title": "Django Development",
                "content": "Best practices for Django projects.",
                "category": "Web Development",
                "tags": ["django", "web"],
            },
            {
                "title": "MongoDB Basics",
                "content": "Introduction to MongoDB and NoSQL databases.",
                "category": "Database",
                "tags": ["mongodb", "database"],
            },
        ]
        cls.collection.insert_many(cls.sample_data)

    @classmethod
    def tearDownClass(cls):
        """
        Clean up MongoDB resources after all tests are completed.
        """
        cls.collection.delete_many({})
        cls.mongo_client.close()
        super().tearDownClass()

    def test_search_with_valid_term(self):
        """
        Test searching for a valid term in the database.
        """
        response = self.client.get(f"{self.blog_url}?search=python")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)  # Ensure results are returned

    def test_search_with_empty_term(self):
        """
        Test searching with an empty search term.
        """
        response = self.client.get(f"{self.blog_url}?search=")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_search_with_no_results(self):
        """
        Test searching for a term that yields no results.
        """
        response = self.client.get(f"{self.blog_url}?search=nonexistentterm")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)  # No results

    def test_search_without_query_param(self):
        """
        Test fetching all posts without a search query parameter.
        """
        response = self.client.get(self.blog_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)  # Fetch all posts
