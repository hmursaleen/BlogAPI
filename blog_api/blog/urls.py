from django.urls import path
from . import views

urlpatterns = [
    path('posts/', views.BlogPostListCreateView.as_view(), name='post-list-create'),
    path('posts/<str:post_id>/', views.BlogPostDetailView.as_view(), name='post-detail'),
]
