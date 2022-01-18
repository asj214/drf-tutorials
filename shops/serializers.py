from rest_framework import serializers
from .models import ShopName


class ShopNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopName
        fields = (
            'id',
            'code',
            'value',
        )