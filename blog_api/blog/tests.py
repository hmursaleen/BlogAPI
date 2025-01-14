from django.core.management.base import BaseCommand
from .models import BlogPost

class Command(BaseCommand):
    help = 'Test the BlogPost class with MongoDB'

    def handle(self, *args, **kwargs):
        blog = BlogPost()
        
        # Create a post
        post_id = blog.create_post(
            title="First Blog Post",
            content="This is the content of the blog post.",
            category="Technology",
            tags=["Python", "Django", "MongoDB"]
        )
        self.stdout.write(f"Created Blog Post ID: {post_id}")

        # Retrieve the post
        post = blog.get_post(post_id)
        self.stdout.write(f"Retrieved Blog Post: {post}")

        # Update the post
        updated_count = blog.update_post(post_id, {"content": "Updated content."})
        self.stdout.write(f"Updated {updated_count} document(s).")

        # Delete the post
        deleted_count = blog.delete_post(post_id)
        self.stdout.write(f"Deleted {deleted_count} document(s).")
