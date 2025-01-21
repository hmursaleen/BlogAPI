from unittest.mock import patch, MagicMock
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status


class BlogPostSearchTests(TestCase):
    @classmethod
    def setUpClass(cls):
        """
        Set up shared test data and API client.
        This runs once for the entire test class.
        """
        super().setUpClass()
        cls.client = APIClient()
        cls.blog_url = "/api/posts/"

        # Example mock data
        cls.sample_data = [
            {
                "_id": "63f1a3c94b516b0ef8c8d5a1",
                "title": "Python Programming",
                "content": "Learn Python programming with examples.",
                "category": "Programming",
                "tags": ["python", "coding"],
                "created_at": "2023-01-01T00:00:00Z",
                "updated_at": "2023-01-01T00:00:00Z",
            },
            {
                "_id": "63f1a3c94b516b0ef8c8d5a2",
                "title": "Django Development",
                "content": "Best practices for Django projects.",
                "category": "Web Development",
                "tags": ["django", "web"],
                "created_at": "2023-01-01T00:00:00Z",
                "updated_at": "2023-01-01T00:00:00Z",
            },
            {
                "_id": "63f1a3c94b516b0ef8c8d5a3",
                "title": "MongoDB Basics",
                "content": "Introduction to MongoDB and NoSQL databases.",
                "category": "Database",
                "tags": ["mongodb", "database"],
                "created_at": "2023-01-01T00:00:00Z",
                "updated_at": "2023-01-01T00:00:00Z",
            },
        ]

    def setUp(self):
        """
        Mock BlogPost's MongoDB dependencies for every test method.
        """
        # Patch the MongoDB initialization in the BlogPost class
        patcher = patch("blog.models.MongoClient")
        #Patched MongoClient to ensure every instance of BlogPost uses the mocked client.
        self.mock_mongo_client = patcher.start()
        self.addCleanup(patcher.stop)

        # Mock the collection object and its methods
        self.mock_collection = MagicMock()
        self.mock_mongo_client.return_value.__getitem__.return_value = {
            "blog_posts": self.mock_collection
        }

        # Set up default return values for the mocked methods
        self.mock_collection.find.return_value = self.sample_data
        self.mock_collection.find_one.return_value = self.sample_data[0]

    def test_search_with_valid_term(self):
        """
        Test searching for a valid term in the database.
        """
        # Simulate a filtered result
        self.mock_collection.find.return_value = [self.sample_data[0]]

        response = self.client.get(f"{self.blog_url}?search=python")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)  # Ensure results are returned
        self.assertIn("title", response.data[0])  # Validate structure

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
        # Simulate no results
        self.mock_collection.find.return_value = []

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
