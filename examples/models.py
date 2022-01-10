from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from conf.models import BaseModel, SoftDeleteModel


class ArtistManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().prefetch_related(
            'user',
            'names'
        ).filter(deleted_at__isnull=True)

    def search_name(self, keyword: str):
        return self.get_queryset().filter(
            id__in=list(set(
                [r.content_id 
                    for r in LocaleName.objects.filter(
                        value__contains=keyword).all()
                ]
            ))
        )


class Artist(BaseModel, SoftDeleteModel):
    user = models.ForeignKey(
        'users.User',
        on_delete=models.DO_NOTHING,
        db_constraint=False,
        default=None,
        null=True,
        related_name='artists'
    )
    name = models.CharField('아티스트명', max_length=200)
    names = GenericRelation(
        'examples.LocaleName',
        default=None,
        null=True,
        object_id_field='content_id',
        content_type_field='content_type'
    )

    objects = ArtistManager()

    class Meta:
        db_table = 'artists'
        ordering = ['-id']
        indexes = []
    
    def __str__(self):
        return f'{self.id}'

    def set_locale_names(self, names: list):
        for row in names:
            self.names.get_or_create(**row)
        return self


class ProductManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().prefetch_related(
            'user',
            'artist',
        ).filter(deleted_at__isnull=True)


class Product(BaseModel, SoftDeleteModel):
    user = models.ForeignKey(
        'users.User',
        on_delete=models.DO_NOTHING,
        db_constraint=False,
        default=None,
        null=True,
        related_name='products'
    )
    name = models.CharField('상품명', max_length=200)
    artist = models.ForeignKey(
        Artist,
        on_delete=models.DO_NOTHING,
        db_constraint=False,
        null=True,
        related_name='products'
    )
    price = models.IntegerField('가격', default=0)

    objects = ProductManager()

    class Meta:
        db_table = 'products'
        ordering = ['-id']
        indexes = []

    def __str__(self):
        return f'{self.id}'


class LocaleName(models.Model):
    content_type = models.ForeignKey(
        ContentType,
        default=None,
        null=True,
        on_delete=models.SET_NULL,
        db_constraint=False,
    )
    content_id = models.PositiveIntegerField(
        default=None,
        null=True,
        blank=True,
        db_column='content_id'
    )

    content_object = GenericForeignKey('content_type', 'content_id')
    code = models.CharField(max_length=200)
    value = models.CharField(max_length=200)

    class Meta:
        db_table = 'locale_names'
        ordering = ['id']
        indexes = [
            models.Index(fields=['content_type', 'content_id'])
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['content_type', 'content_id', 'code'],
                name='unique_locale_name'
            )
        ]

    def __str__(self):
        return f'{self.id}'