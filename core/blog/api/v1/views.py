from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import (IsAdminUser, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly,)
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .serializers import PostSerializer, CategorySerializer,PostCommentSerializer
from ...models import Post,Category,PostComment


# 1. API function base view (FBV)
"""
@api_view(['GET','POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def postList(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    

@api_view(['GET','PUT','DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def postDetail(request,pk):
    post = get_object_or_404(Post, pk=pk, status=True)    
    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = PostSerializer(post,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    elif request.method == 'DELETE':
        post.delete()
        return Response({'details':'The item successfully deleted.'},status=status.HTTP_204_NO_CONTENT)
"""    
    
 

from rest_framework.permissions import (IsAdminUser, IsAuthenticated,IsAuthenticatedOrReadOnly,)
from rest_framework.views import APIView

# 2. APIView in CBV
"""
class PostList(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer
    def get(self,request):
        posts = Post.objects.filter(status=True)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    

class PostDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer
        
    '''retriving'''
    '''
    def get_object(self,pk):
        post = get_object_or_404(Post, pk=pk, status=True)
        return post
    '''
        
    '''retriving'''
    def get(self,request,pk):
        # post = self.get_object(pk)
        post = get_object_or_404(Post, pk=pk, status=True)
        # serializer = PostSerializer(post)
        serializer = self.serializer_class(post)
        return Response(serializer.data)
    
    '''editing'''
    def put(self,request,pk):
        post = get_object_or_404(Post, pk=pk, status=True)
        serializer = PostSerializer(post,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    '''deleting'''
    def delete(self,request,pk):
        post = get_object_or_404(Post, pk=pk, status=True)
        post.delete()
        return Response({'details':'The item successfully deleted.'},status=status.HTTP_204_NO_CONTENT)
"""



from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import mixins

# 3. GenericAPIView in CBV
"""
'''
class Postlist(GenericAPIView,mixins.ListModelMixin,mixins.CreateModelMixin):
'''
class PostListCreateAPIView(ListCreateAPIView):
    queryset = Post.objects.filter(status=True)
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
'''  
class PostDetail(GenericAPIView,mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin):
'''
class PostRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.filter(status=True)
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
"""
    

from rest_framework import viewsets


# 4. ModelViewSet in CBV
# 4.1 viewsets.ViewSet
"""
class PostViewSet(viewsets.ViewSet):
    queryset = Post.objects.filter(status=True)
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def list(self,request):
        posts = self.queryset
        serializer = self.serializer_class(posts, many=True)
        return Response(serializer.data)
    
    def create(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    
    def retrieve(self,request,pk=None):
        post = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(post)
        return Response(serializer.data)    
    
    def update(self,request,pk=None):
        post = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(post,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def partial_update(self,request,pk=None):
        post = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(post,data=request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def destroy(self,request,pk=None):
        post = get_object_or_404(self.queryset, pk=pk)
        post.delete()
        return Response({'details':'The item successfully deleted.'},status=status.HTTP_204_NO_CONTENT)
"""


from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter ,OrderingFilter
from rest_framework.decorators import action
from .paginations import CustomPagination
from .permissions import IsOwnerOrReadOnly
# from .filters import PostFilter


# 4.2 viewsets.ModelViewSet (Router Structure)

class PostModelViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.filter(status=True)
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    # filterset_classes = PostFilter
    filterset_fields = ['author','topic','category','status']
    search_fields = ['title','content']
    ordering_fields = ['published_date','counted_views']
    pagination_class = CustomPagination
    
    @action(detail=False, methods=['get'])
    def latest_posts(self, request):
        latest_posts = self.queryset.order_by('-published_date')[:2]
        serializer = self.serializer_class(latest_posts, many=True, context={'request':request})
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def latest_post(self, request, pk=None):
        latest_post = self.queryset.order_by('-published_date')[:2]
        serializer = self.serializer_class(latest_post, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def most_views(self, request, pk=None):
        most_views = self.queryset.order_by('-counted_views')[:2]
        serializer = self.serializer_class(most_views, many=True, context={'request':request})
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def posts_author(self, request, pk=None):
        posts_author = self.queryset.filter(author=pk)
        serializer = self.serializer_class(posts_author, many=True, context={'request':request})
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def posts_category(self, request, pk=None):
        posts_category = self.queryset.filter(category=pk)
        serializer = self.serializer_class(posts_category, many=True, context={'request':request})
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def posts_topic(self, request, pk=None):
        posts_topic = self.queryset.filter(topic=pk)
        serializer = self.serializer_class(posts_topic, many=True, context={'request':request})
        return Response(serializer.data)
    
   
class PostCommentModelViewSet(viewsets.ModelViewSet):
    queryset = PostComment.objects.all()
    serializer_class = PostCommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]
    
    
    
    
    
    # def get_queryset(self):
    #     return self.queryset.filter(author=self.request.user)
    
    # def perform_create(self, serializer):
    #     serializer.save(author=self.request.user)
    
    # def get_permissions(self):
    #     if self.action == 'create':
    #         permission_classes = [IsAuthenticated]
    #     elif self.action in ['update','partial_update','destroy']:
    #         permission_classes = [IsAuthenticated]
    #     else:
    #         permission_classes = [IsAuthenticatedOrReadOnly]
    #     return [permission() for permission in permission_classes]
    
    # def get_serializer_class(self):
    #     if self.action == 'list':
    #         return PostSerializer
    #     elif self.action == 'retrieve':
    #         return PostSerializer
    #     return PostSerializer


class CategoryModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()