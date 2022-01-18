from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Category
from .serializers import CategorySerializer, CategoryListSerializer


class CategoryListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CategoryListSerializer
    queryset = Category.objects.prefetch_related('children').all()

    def get_queryset(self):
        return self.queryset.filter(depth=1)

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        context = {'user': request.user}
        serializer = self.serializer_class(
            data=request.data,
            context=context,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CategoryView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CategorySerializer
    queryset = Category.objects.prefetch_related('user').all()

    def get_queryset(self):
        return self.queryset
    
    def get_object(self, pk=None):
        try:
            return self.queryset.get(pk=pk)
        except Category.DoesNotExist:
            raise NotFound('Not Found')

    def get(self, request, pk=None, *args, **kwargs):
        category = self.get_object(pk)
        serializer = self.serializer_class(category)

        return Response(serializer.data)

    def put(self, request, pk=None, *args, **kwargs):
        category = self.get_object(pk)
        serializer = self.serializer_class(
            category,
            data=request.data,
            context={'user': request.user},
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def delete(self, request, pk=None, *args, **kwargs):
        category = self.get_object(pk)
        category.recursive_remove()

        return Response(status=status.HTTP_204_NO_CONTENT)