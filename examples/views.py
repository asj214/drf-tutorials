from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from .models import Artist, Product
from .serializers import (
    ArtistSerializer,
    ProductSerializer
)


class ArtistViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ArtistSerializer
    queryset = Artist.objects

    def get_queryset(self):
        qs = self.queryset
        name = self.request.query_params.get('name')
        if name:
            qs = qs.search_name(name)

        return qs.all()
    
    def get_object(self, pk):
        try:
            return self.get_queryset().get(pk=pk)
        except Artist.DoesNotExist:
            raise NotFound('Not Found')

    def list(self, request, *args, **kwargs):
        page = self.paginate_queryset(self.get_queryset())
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)
    
    def create(self, request, pk=None, *args, **kwargs):
        context = {
            'user': request.user,
            'names': request.data.pop('names', [])
        }
        serializer = self.serializer_class(
            data=request.data,
            context=context,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None, *args, **kwargs):
        artist = self.get_object(pk)
        serializer = self.serializer_class(artist)

        return Response(serializer.data)
    
    def update(self, request, pk=None, *args, **kwargs):
        artist = self.get_object(pk)
        context = {
            'user': request.user,
            'names': request.data.pop('names', [])
        }

        serializer = self.serializer_class(
            artist,
            data=request.data,
            context=context,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
    
    def destroy(self, request, pk=None, *args, **kwargs):
        artist = self.get_object(pk)
        artist.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def get_queryset(self):
        return self.queryset


    def get_object(self, pk):
        try:
            return self.get_queryset().get(pk=pk)
        except Product.DoesNotExist:
            raise NotFound('Not Found')


    def list(self, request, *args, **kwargs):
        page = self.paginate_queryset(self.get_queryset())
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)


    def create(self, request, pk=None, *args, **kwargs):
        context = {
            'user': request.user,
            'names': request.data.pop('names', [])
        }
        serializer = self.serializer_class(
            data=request.data,
            context=context,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


    def retrieve(self, request, pk=None, *args, **kwargs):
        product = self.get_object(pk)
        serializer = self.serializer_class(product)

        return Response(serializer.data)


    def update(self, request, pk=None, *args, **kwargs):
        context = {
            'user': request.user,
            'names': request.data.pop('names', [])
        }
        product = self.get_object(pk)
        serializer = self.serializer_class(
            product,
            data=request.data,
            context=context,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


    def destroy(self, request, pk=None, *args, **kwargs):
        product = self.get_object(pk)
        product.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)