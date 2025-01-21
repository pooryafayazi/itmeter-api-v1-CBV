# from django import template
# from blog.models import Post,PostComment
# register = template.Library()
# from blog.models import Category
# from django.utils import timezone

# @register.inclusion_tag('blog/popular-posts.html')
# def latest_posts(arg=3):
#     posts = Post.objects.filter(status=1, published_date__lte=timezone.now()).order_by('-counted_views')[:arg]
#     return {'posts' : posts}


# @register.inclusion_tag('home/categories.html')
# def postcategories():
#     posts = Post.objects.filter(status=1, published_date__lte=timezone.now())
#     categories = Category.objects.all()
    
#     cat_list = [] 
#     for category in categories:
#         count = posts.filter(category=category).count() 
#         cat_list.append({'name': category.name, 'count': count}) 
#     cat_list.sort(key=lambda x: x['count'], reverse=True)
#     return {'Pcategories': cat_list} 