from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import (IsAdminUser, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly,)
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .serializers import PostSerializer
from ...models import Post


# 1. API function base view (FBV)

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
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
        return Response({'details':'Item successfully deleted.'},status=status.HTTP_204_NO_CONTENT)
    
    
    
# 2. API view 


# 3. Generic API view



# 4. Model Viewset in CBV
    

from rest_framework.permissions import (IsAdminUser, IsAuthenticated,IsAuthenticatedOrReadOnly,
                                        DjangoModelPermissionsOrAnonReadOnly)
from rest_framework.decorators import permission_classes
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import mixins,viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter ,OrderingFilter
# from .paginations import CustomPagination
# from .permissions import IsOwnerOrReadOnly
# from .filters import TaskFilter

class PostModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]