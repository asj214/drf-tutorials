from rest_framework import serializers
from .models import Brand, Product
from users.serializers import UserSerializer


class BrandSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    name = serializers.CharField(max_length=200)
    is_active = serializers.BooleanField(default=False)

    class Meta:
        model = Brand
        fields = (
            'id',
            'user',
            'name',
            'is_active',
            'created_at',
            'updated_at'
        )
    
    def create(self, validated_data):
        user = self.context.get('user')
        return Brand.objects.create(
            user=user,
            **validated_data
        )
    
    def update(self, instance, validated_data):
        user = self.context.get('user')
        for (key, value) in validated_data.items():
            setattr(instance, key, value)
        
        instance.user = user
        instance.save()

        return instance


class ProductSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    brand = BrandSerializer(read_only=True)
    name = serializers.CharField(max_length=200)
    is_published = serializers.BooleanField(default=False)

    class Meta:
        model = Product
        fields = (
            'id',
            'code',
            'type',
            'user',
            'brand',
            'name',
            'price',
            'content',
            'is_sale_period',
            'started_at',
            'finished_at',
            'status',
            'is_published',
            'created_at',
            'updated_at'
        )
    
    def create(self, validated_data):
        user = self.context.get('user')
        brand_id = self.context.get('brand_id', None)

        product = Product.objects.create(
            user=user,
            brand_id=brand_id,
            **validated_data
        )
        product.make_code()

        return product
    
    def update(self, instance, validated_data):
        user = self.context.get('user')
        brand_id = self.context.get('brand_id', None)

        for (key, value) in validated_data.items():
            setattr(instance, key, value)
        
        instance.user = user
        if brand_id:
            instance.brand_id = brand_id
        instance.save()

        return instance