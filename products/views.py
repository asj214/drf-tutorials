from rest_framework import status, viewsets, generics
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Brand, Product, MongoProduct
from .serializers import BrandSerializer, ProductSerializer


class BrandViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = BrandSerializer
    queryset = Brand.objects.prefetch_related('user').all()

    def get_queryset(self):
        return self.queryset
    
    def get_object(self, pk=None):
        try:
            return self.queryset.get(pk=pk)
        except Brand.DoesNotExist:
            raise NotFound('Not Found')
    
    def list(self, request, *args, **kwargs):
        page = self.paginate_queryset(self.get_queryset())
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def create(self, request, *args, **kwargs):
        context = {
            'user': request.user,
        }
        serializer = self.serializer_class(
            data=request.data,
            context=context,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None, *args, **kwargs):
        brand = self.get_object(pk)
        serializer = self.serializer_class(brand)

        return Response(serializer.data)

    def update(self, request, pk=None, *args, **kwargs):
        brand = self.get_object(pk)
        serializer = self.serializer_class(
            brand,
            data=request.data,
            context={'user': request.user},
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def destroy(self, request, pk=None, *args, **kwargs):
        brand = self.get_object(pk)
        brand.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ProductSerializer
    queryset = Product.objects.prefetch_related('user', 'brand__user').all()

    def get_queryset(self):
        return self.queryset
    
    def get_object(self, pk=None):
        try:
            return self.queryset.get(pk=pk)
        except Product.DoesNotExist:
            raise NotFound('Not Found')
    
    def list(self, request, *args, **kwargs):
        page = self.paginate_queryset(self.get_queryset())
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    def create(self, request, *args, **kwargs):
        context = {
            'user': request.user,
            'brand_id': request.data.pop('brand_id', None)
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
        product = self.get_object(pk)
        serializer = self.serializer_class(
            product,
            data=request.data,
            context={
                'user': request.user,
                'brand_id': request.data.pop('brand_id', None)
            },
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def destroy(self, request, pk=None, *args, **kwargs):
        product = self.get_object(pk)
        product.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductApprovalView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ProductSerializer
    queryset = Product.objects.prefetch_related('user', 'brand__user').all()

    def get_object(self, pk=None):
        try:
            return self.queryset.get(pk=pk)
        except Product.DoesNotExist:
            raise NotFound('Not Found')
    
    def update(self, request, pk=None, *args, **kwargs):
        product = self.get_object(pk)
        product.approval()

        serializer = self.serializer_class(product)

        document = MongoProduct()
        document.create(**serializer.data)
        
        return Response(serializer.data)