from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from rest_framework.exceptions import NotFound


class PostManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().prefetch_related(
            'user',
            'comments'
        ).filter(deleted_at__isnull=True)


class Post(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        db_constraint=False,
        default=None,
        null=True,
        related_name='posts'
    )
    title = models.CharField('제목', max_length=200)
    body = models.TextField('본문')
    comments = GenericRelation(
        'comments.Comment',
        default=None,
        null=True,
        object_id_field='commentable_id',
        content_type_field='commentable_type'
    )

    created_at = models.DateTimeField('등록일', auto_now_add=True)
    updated_at = models.DateTimeField('수정일', auto_now=True)
    deleted_at = models.DateTimeField('삭제일', null=True, default=None)

    objects = PostManager()

    class Meta:
        db_table = 'posts'
        ordering = ['-id']
        indexes = []
    
    def __str__(self):
        return f'{self.id}'

    def add_comment(self, user, params: dict = {}):
        self.comments.create(
            user=user,
            body=params.get('body')
        )

    def set_comment(self, id=None, params: dict = {}):
        try:
            comment = self.comments.get(pk=id)
            comment.body = params.get('body')
            comment.save()
        except ObjectDoesNotExist:
            raise NotFound('Not Found')
    
    def remove_comment(self, id=None):
        try:
            comment = self.comments.get(pk=id)
            comment.delete()
        except ObjectDoesNotExist:
            raise NotFound('Not Found')