from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from rest_framework.exceptions import ParseError
from bson.objectid import ObjectId
from blog.models import BlogPost
from blog.serializers import BlogPostSerializer
#from django.utils.http import urlencode
from bson.regex import Regex

'''
see if you can write blog = BlogPost() only once in the beginning of the class
'''
class BlogPostListCreateView(APIView):
    def get(self, request):
        blog = BlogPost()
        #posts = blog.collection.find()  # Fetch all posts
        filters = {}

        try:
            search_term = request.query_params.get('search', None)  # fetches the search parameter from the request URL.
            if search_term == '':
                return Response({"error": "Search term can't be empty"}, status=status.HTTP_400_BAD_REQUEST)
            
            # Create a MongoDB case-insensitive regex for filtering

            if search_term is not None:
                regex = Regex(search_term, 'i')  # 'i' is for case-insensitive
                filters = {
                    '$or': [  # Perform an OR search across multiple fields
                        {'title': regex},
                        {'content': regex},
                        {'category': regex},
                    ]
                }

            posts = blog.collection.find(filters)  # Apply filters to MongoDB query
            posts = [
                {
                    **post,
                    #'id': str(post['_id']),  # Convert ObjectId to string
                    '_id': str(post['_id'])  # Include _id if required
                } for post in posts
            ]
            return Response(posts, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": "An unexpected error occurred.", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        serializer = BlogPostSerializer(data=request.data)
        if serializer.is_valid():
            blog = BlogPost()
            post_id = blog.create_post(
                title=serializer.validated_data['title'],
                content=serializer.validated_data['content'],
                category=serializer.validated_data['category'],
                tags=serializer.validated_data['tags'],
            )
            return Response({'id': str(post_id)}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BlogPostDetailView(APIView):
    def get(self, request, post_id):
        blog = BlogPost()
        post = blog.get_post(post_id)
        if not post:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
        post['id'] = str(post['_id'])
        del post['_id']
        return Response(post, status=status.HTTP_200_OK)

    def put(self, request, post_id):
        serializer = BlogPostSerializer(data=request.data)
        if serializer.is_valid():
            blog = BlogPost()
            updated_count = blog.update_post(post_id, serializer.validated_data)
            if updated_count == 0:
                return Response({'error': 'Post not found or not updated'}, status=status.HTTP_404_NOT_FOUND)
            return Response({'message': 'Post updated successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, post_id):
        blog = BlogPost()
        deleted_count = blog.delete_post(post_id)
        if deleted_count == 0:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'message': 'Post deleted successfully'}, status=status.HTTP_204_NO_CONTENT)





'''
5. Optional Enhancements
Additional Filters:

Add more query parameters for filtering by specific fields like category or tags.
Sorting:

Support sorting by fields like created_at or title using query parameters.
Complex Search:

Extend the search functionality to support partial matches for tags or advanced filtering logic.
'''