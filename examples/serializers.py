from django.db import transaction
from rest_framework import serializers
from .models import Artist, Product, LocaleName
from users.serializers import UserSerializer


class LocaleRelatedSerializer(serializers.ModelSerializer):
    code = serializers.CharField(max_length=200)
    value = serializers.CharField(max_length=200)

    class Meta:
        model = LocaleName
        fields = (
            'code',
            'value',
        )

class ArtistRelated(serializers.ModelSerializer):
    name = serializers.CharField(max_length=200)
    
    class Meta:
        model = Artist
        exclude = (
            'user',
        )


class ArtistSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=200)
    names = LocaleRelatedSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Artist
        fields = '__all__'

    def create(self, validated_data):
        user = self.context.pop('user')
        return Artist.objects.create(
            user=user,
            **validated_data
        )

    def update(self, instance, validated_data):
        with transaction.atomic():
            user = self.context.pop('user')
            for (key, value) in validated_data.items():
                setattr(instance, key, value)

            instance.user = user
            instance.set_locale_names(self.context.pop('names', []))
            instance.save()

        return instance


class ProductSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    name = serializers.CharField(max_length=200)
    price = serializers.IntegerField(default=0)
    artist = ArtistRelated(read_only=True)

    class Meta:
        model = Product
        exclude = (
            'deleted_at',
        )

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['artist'] = ArtistRelated(instance.artist).data
        return response

    def create(self, validated_data):
        user = self.context.pop('user')
        return Product.objects.create(
            user=user,
            **validated_data
        )

    def update(self, instance, validated_data):
        user = self.context.pop('user')
        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        instance.user = user



        instance.save()

        return instance