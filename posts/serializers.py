from rest_framework import serializers
from .models import Post
from users.serializers import UserSerializer
# from comments.serializers import CommentSerializer


class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    title = serializers.CharField(max_length=200)
    body = serializers.CharField()
    # comments = CommentSerializer(read_only=True, many=True)

    class Meta:
        model = Post
        fields = (
            'id',
            'user',
            'title',
            'body',
            # 'comments',
            'created_at',
            'updated_at'
        )

    def create(self, validated_data):
        user = self.context.pop('user')
        return Post.objects.create(
            user=user,
            **validated_data
        )

    def update(self, instance, validated_data):
        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        instance.save()
        return instance
