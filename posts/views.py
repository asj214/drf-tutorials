from rest_framework import status, viewsets, generics
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly
)
from rest_framework.views import APIView
from .models import Post
from .serializers import PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def get_queryset(self):
        return self.queryset
    
    def get_object(self, pk=None):
        try:
            return self.get_queryset().get(pk=pk)
        except Post.DoesNotExist:
            raise NotFound('Not Found')
    
    def list(self, request, *args, **kwargs):
        page = self.paginate_queryset(self.get_queryset())
        serializer = self.get_serializer(page, many=True)

        return self.get_paginated_response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        context = {'user': request.user}
        serializer = self.serializer_class(
            data=request.data,
            context=context
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None, *args, **kwargs):
        post = self.get_object(pk)
        serializer = self.serializer_class(post)

        return Response(serializer.data)

    def update(self, request, pk=None, *args, **kwargs):
        post = self.get_object(pk)
        serializer = self.serializer_class(
            post,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data) 

    def destroy(self, request, pk=None, *args, **kwargs):
        post = self.get_object(pk)
        post.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class PostCommentCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def get_object(self, pk=None):
        try:
            return self.get_queryset().get(pk=pk)
        except Post.DoesNotExist:
            raise NotFound('Not Found')

    def post(self, request, pk=None, *args, **kwargs):
        post = self.get_object(pk)
        post.add_comment(
            user=request.user,
            params=request.data
        )
        serializer = self.serializer_class(post)

        return Response(serializer.data)


class PostCommentView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def get_object(self, pk=None, id=None):
        try:
            return self.queryset.get(pk=pk)
        except Post.DoesNotExist:
            raise NotFound('Not Found')

    def put(self, request, pk=None, id=None, *args, **kwargs):
        post = self.get_object(pk)
        post.set_comment(id, request.data)
        serializer = self.serializer_class(post)

        return Response(serializer.data)

    def delete(self, request, pk=None, id=None, *args, **kwargs):
        post = self.get_object(pk)
        post.remove_comment(id)

        serializer = self.serializer_class(post)

        return Response(serializer.data)