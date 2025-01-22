from rest_framework import serializers
from blog.models import Post

class PostSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ['id','image','author','title','topic','content','tags','category','counted_views','status','login_require','published_date']
        # fields = '__all__'
    def get_tags(self, obj):
        return list(obj.tags.names())  # Convert tags to a list of tag names