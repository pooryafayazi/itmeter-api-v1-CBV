from django.urls import path,include
from . import views

app_name = 'api-v1'

urlpatterns = [
    # 1. API function base view (FBV)
    # path('posts/', views.postList, name='post_list'),   
    # path('post/<int:pk>/', views.postDetail, name='post_detail'),
    
    # 2. APIView in CBV
    # path('posts/', views.PostList.as_view(), name='post_list'),
    # path('post/<int:pk>/', views.PostDetail.as_view(), name='post_detail'),
    
    
    # 3. GenericAPIView in CBV
    # path('posts/', views.PostListCreateAPIView.as_view(), name='post_list'),
    # path('post/<int:pk>/', views.PostRetrieveUpdateDestroyAPIView.as_view(), name='post_detail'),
    
    
    # 4. ModelViewSet in CBV
    # 4.1 viewsets.ViewSet
    # path('posts/', views.PostViewSet.as_view({'get':'list','post':'create'}), name='post_list'),
    # path('posts/<int:pk>', views.PostViewSet.as_view({'get':'retrieve','put':'update','patch':'partial_update','delete':'destroy'}), name='post_list'),
        
]


    # 4.2 viewsets.ModelViewSet
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
# router.register('posts', views.PostViewSet, basename='post')
router.register('posts', views.PostModelViewSet, basename='post')
router.register('categories', views.CategoryModelViewSet, basename='category')
router.register('comments', views.PostCommentModelViewSet, basename='comment')
urlpatterns += router.urls
'''
urlpatterns += [
    path('',include(router.urls)),
]
'''