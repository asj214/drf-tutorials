from rest_framework import serializers
from .models import Comment
from users.serializers import UserSerializer


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = (
            'id',
            'user',
            'body',
            'created_at',
            'updated_at'
        )
    
    def create(self, validated_data):
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)