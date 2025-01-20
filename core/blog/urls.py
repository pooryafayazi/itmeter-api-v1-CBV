from django.urls import path,include
# from .views import api_task_list_view
from . import views
from rest_framework.routers import DefaultRouter

app_name = 'blog'

router = DefaultRouter()
# router.register('blog', views.BlogModelViewSet, basename='blog')



urlpatterns = [
    # path('task/', views.api_task_list_view,name='api-task-list'),
    # path('task/', views.TaskList, name='task-list'),
    # path('task/', views.TaskList.as_view(), name='task-list'),
    # path('task/<int:id>/', views.taskDetail, name='task-detail'),
    # path('task/<int:pk>/', views.TaskDetail.as_view(), name='task-detail'),
    # path('task/', views.TaskViewSet.as_view({'get':'list','post':'create'}), name='task-list'),
    # path('task/<int:pk>/', views.TaskViewSet.as_view({'get':'retrieve','put':'update','patch':'partial_update','delete':'destroy'}), name='task-list'),
]

urlpatterns += router.urls

urlpatterns += [
    path('posts/', views.PostListView.as_view(), name='post_list'),
    path('create/', views.PostCreateView.as_view(), name='post-create'),
    path('edit/<int:pk>/', views.PostUpdateView.as_view(), name='post-update'),
    path('delete/<int:pk>/', views.PostDeleteView.as_view(), name='post-delete'),
    path('complete/<int:pk>/', views.PostCompleteView.as_view(), name='post-complete'),
    # path('api/v1/',include('tasks.api.v1.urls')),
]