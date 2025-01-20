from django.db import models
# from django.conf import settings
# from django.contrib.auth import get_user_model
# from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
 
# User = get_user_model()

        
        
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name
    
    
class Post(models.Model):
    # image = models.ImageField(upload_to='blog/%Y/%m/%d/',default='blog/defaultPost.jpg')
    image = models.ImageField(null=True, blank=True)
    #author = models.ForeignKey(User, on_delete=models.CASCADE)
    author = models.ForeignKey('accounts.Profile', on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255)
    topic = models.ForeignKey('homepage.Topic', on_delete=models.SET_NULL, null=True)
    content = models.TextField()
    tags = TaggableManager()
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    counted_views = models.IntegerField(default=0) # default=0
    status = models.BooleanField(default=False)
    login_require = models.BooleanField(default=False)
    published_date = models.DateTimeField(null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ('-created_date',)
        #verbose_name = "پست"
        #verbose_name_plural = "پست ها"
    def __str__(self):
        return f'{self.title} - {self.id}'

    def snippets(self):
        return self.content[:100]
    
    def get_absolute_url(self):
        return reverse('blog:single', kwargs={'post_id':self.id})
    

class PostComment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    def __str__(self):
        return f'{self.name} - post : {self.post}'
    class Meta:
        ordering = ('-created_date',)