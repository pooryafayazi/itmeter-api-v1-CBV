from django.urls import path,include
from . import views

app_name = 'api-v1'


urlpatterns = [
    path('posts/', views.postList, name='post_list'),   
    path('post/<int:pk>/', views.postDetail, name='post_detail'),   
]