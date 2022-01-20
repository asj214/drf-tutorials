from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from conf.models import BaseModel, SoftDeleteModel


class ShopManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def active(self):
        return self.get_queryset().filter(is_active=True)


class Shop(BaseModel, SoftDeleteModel):
    user = models.ForeignKey(
        'users.User',
        on_delete=models.DO_NOTHING,
        db_constraint=False,
        default=None,
        null=True,
        related_name='shops'
    )
    code = models.CharField('상점코드', max_length=10)
    name = models.CharField('상점명', max_length=200)
    order = models.IntegerField('순서', default=99)
    is_active = models.BooleanField('사용여부', default=True)

    objects = ShopManager()

    class Meta:
        db_table = 'shops'
        ordering = ['order', '-id']
        indexes = [
            models.Index(fields=['is_active', 'deleted_at'])
        ]


class ShopNameManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def search_name(self, keyword: str):
        return list(set(
            [r.content_id for r in self.get_queryset().filter(
                value__contains=keyword).all()]
        ))


class ShopName(BaseModel):
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

    objects = ShopNameManager()

    class Meta:
        db_table = 'shop_names'
        ordering = ['id']
        indexes = [
            models.Index(fields=['content_type', 'content_id'])
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['content_type', 'content_id', 'code'],
                name='unique_nameable'
            )
        ]

    def __str__(self):
        return f'{self.id}'