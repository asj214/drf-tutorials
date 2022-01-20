from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from conf.models import BaseModel, SoftDeleteModel


class Category(BaseModel, SoftDeleteModel):
    parent = models.ForeignKey(
        'self',
        on_delete=models.DO_NOTHING,
        db_constraint=False,
        default=None,
        null=True,
        related_name='children'
    )
    name = models.CharField('카테고리명', max_length=200)
    names = GenericRelation(
        'shops.ShopName',
        default=None,
        null=True,
        object_id_field='content_id',
        content_type_field='content_type'
    )
    user = models.ForeignKey(
        'users.User',
        on_delete=models.DO_NOTHING,
        db_constraint=False,
        default=None,
        null=True,
        related_name='categories'
    )
    depth = models.IntegerField('뎁스', default=0)
    order = models.IntegerField('순서', default=1)
    is_active = models.BooleanField('사용여부', default=True)
    path = models.JSONField('계보', null=True, default=None)

    class Meta:
        db_table = 'categories'
        ordering = ['-id']
        indexes = [
            models.Index(fields=['is_active', 'deleted_at'])
        ]

    def recursive_remove(self):
        for child in self.children.all():
            child.remove()
        self.delete()

    def make_path(self, path: list = []):
        path.append(self.name)
        if self.parent_id is None:
            return list(reversed(path))
        else:
            return self.parent.make_path(path)
    
    def set_path(self):
        self.path = self.make_path(path=[])
        self.save()