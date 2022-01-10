from django.db import models
from conf.models import BaseModel, SoftDeleteModel


class PostManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().prefetch_related(
            'user',
        ).filter(deleted_at__isnull=True)


class Post(BaseModel, SoftDeleteModel):
    user = models.ForeignKey(
        'users.User',
        on_delete=models.DO_NOTHING,
        db_constraint=False,
        default=None,
        null=True,
        related_name='posts'
    )
    title = models.CharField('제목', max_length=200)
    body = models.TextField('본문')

    objects = PostManager()

    class Meta:
        db_table = 'posts'
        ordering = ['-id']
        indexes = []
    
    def __str__(self):
        return f'{self.id}'
