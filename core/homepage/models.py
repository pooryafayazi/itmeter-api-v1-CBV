from django.db import models
from django.urls import reverse
from blog.models import Category
# from taggit.managers import TaggableManager

# Create your models here.
class Contact(models.Model):
    name= models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField()
    subject = models.CharField(max_length=255, blank=True, null=True)
    message = models.TextField()
    creator = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-created_date']
    def __str__(self):
        return self.email
    
class Newsletter(models.Model):
    email = models.EmailField()
    def __str__(self):
        return self.email
class Topic(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name

class News(models.Model):
    # image = models.ImageField(upload_to='news/%Y/%m/%d/',default='news/defaultPost.jpg')
    #author = models.ForeignKey(User, on_delete=models.CASCADE)
    author = models.ForeignKey('accounts.Profile', on_delete=models.SET_NULL, null=True)
    source = models.URLField()
    title = models.CharField(max_length=255)
    content = models.TextField()
    # tags = TaggableManager()
    category = models.ManyToManyField(Category)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=True)
    counted_views = models.IntegerField(default=0) # default=0
    status = models.BooleanField(default=False)
    published_date = models.DateTimeField(null=True)
    class Meta:
        ordering = ('-published_date',)
        #verbose_name = "پست"
        verbose_name_plural = "News"
    def __str__(self):
        return f'{self.title} - {self.id}'

    def snippets(self):
        return self.content[:100]
    
    def get_absolute_url(self):
        return reverse('homepage:news', kwargs={'news_id':self.id})
    
class newsComment(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    def __str__(self):
        return f'{self.name} - post : {self.news}'
    class Meta:
        ordering = ('-created_date',)