from rest_framework import filters
from blog.models import Post

class PostFilter(filters.BaseFilterBackend):
    class Meta:
        model = Post
        fields = ['author','topic','category','status']