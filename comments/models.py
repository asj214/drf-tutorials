from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class CommentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().prefetch_related('user').filter(deleted_at__isnull=True)


class Comment(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        db_constraint=False,
        default=None,
        null=True,
        related_name='comments'
    )
    commentable_type = models.ForeignKey(
        ContentType,
        default=None,
        null=True,
        on_delete=models.SET_NULL,
        db_constraint=False,
        db_column='commentable_type'
    )
    commentable_id = models.PositiveIntegerField(
        default=None,
        null=True,
        blank=True,
        db_column='commentable_id'
    )
    commentable = GenericForeignKey('commentable_type', 'commentable_id')

    body = models.CharField('본문', max_length=255)
    created_at = models.DateTimeField('등록일', auto_now_add=True)
    updated_at = models.DateTimeField('수정일', auto_now=True)
    deleted_at = models.DateTimeField('삭제일', null=True, default=None)

    class Meta:
        db_table = 'comments'
        ordering = ['-id']
        indexes = [
            models.Index(fields=['commentable_type', 'commentable_id', 'deleted_at']),
        ]
    
    def __str__(self):
        return f'{self.id}'