from rest_framework import serializers
from conf.serializers import RecursiveField
from users.serializers import UserSerializer
from shops.serializers import ShopNameSerializer
from .models import Category


class CategoryListSerializer(serializers.ModelSerializer):
    parent_id = serializers.IntegerField(write_only=True, allow_null=True)
    name = serializers.CharField(max_length=200)
    depth = serializers.IntegerField(default=0)
    order = serializers.IntegerField(default=1)
    is_active = serializers.BooleanField(default=False)
    childrens = RecursiveField(many=True, read_only=True, source='children')

    class Meta:
        model = Category
        fields = (
            'id',
            'parent_id',
            'name',
            'depth',
            'order',
            'is_active',
            'created_at',
            'updated_at',
            'childrens'
        )
    
    def create(self, validated_data):
        user = self.context.get('user')
        category = Category.objects.create(
            user=user,
            **validated_data
        )

        category.set_path()

        return category

class CategorySerializer(serializers.ModelSerializer):
    parent_id = serializers.IntegerField(write_only=True, allow_null=True)
    user = UserSerializer(read_only=True)
    name = serializers.CharField(max_length=200)
    names = ShopNameSerializer(many=True)
    depth = serializers.IntegerField(default=0)
    order = serializers.IntegerField(default=1)
    is_active = serializers.BooleanField(default=False)
    path = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = (
            'id',
            'parent_id',
            'name',
            'names',
            'user',
            'path',
            'depth',
            'order',
            'is_active',
            'created_at',
            'updated_at',
        )

    def get_path(self, instance):
        return ' > '.join(instance.path)

    def update(self, instance, validated_data):
        user = self.context.get('user')
        for (key, value) in validated_data.items():
            setattr(instance, key, value)
        
        instance.user = user
        instance.set_path()
        instance.save()

        return instance