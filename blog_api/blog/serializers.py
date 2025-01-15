from rest_framework import serializers

'''
This serializer validates input data for creating and updating blog posts.
It ensures compatibility with DRF's response and request handling.
'''
#See if you can serialize all fields at one in a list like [id, title, content ...]
class BlogPostSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    title = serializers.CharField(max_length=200)
    content = serializers.CharField()
    category = serializers.CharField(max_length=100)
    tags = serializers.ListField(
        child=serializers.CharField(max_length=50),
        allow_empty=True
    )
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
