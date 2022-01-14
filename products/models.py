from django.db import models
from conf.models import BaseModel, SoftDeleteModel
from conf.mongodb import MongoModel


class Brand(BaseModel, SoftDeleteModel):
    user = models.ForeignKey(
        'users.User',
        on_delete=models.DO_NOTHING,
        db_constraint=False,
        default=None,
        null=True,
        related_name='brands'
    )
    name = models.CharField('브랜드명', max_length=200)
    is_active = models.BooleanField('사용여부', default=True)

    class Meta:
        db_table = 'brands'
        ordering = ['-id']
        indexes = [
            models.Index(fields=['is_active', 'deleted_at'])
        ]


class Product(BaseModel, SoftDeleteModel):
    PRODUCT_TYPE = (
        ('GENERAL', '일반상품'),
        ('OPTION', '옵션상품'),
        ('PACKAGE', '패키지상품'),
    )
    STATUS_CHOICE = (
        ('TEMP_STORAGE', '임시저장'),
        ('WAIT', '승인대기'),
        ('APPROVAL', '승인'),
    )
    code = models.CharField('상품 코드 Ex. PR00000001', max_length=30, null=True, default=None, blank=True)
    type = models.CharField('상품 유형', max_length=10, choices=PRODUCT_TYPE)

    user = models.ForeignKey(
        'users.User',
        on_delete=models.DO_NOTHING,
        db_constraint=False,
        default=None,
        null=True,
        related_name='products'
    )
    brand = models.ForeignKey(
        'products.Brand',
        on_delete=models.DO_NOTHING,
        db_constraint=False,
        default=None,
        null=True,
        related_name='products'
    )

    name = models.CharField('상품명', max_length=200)
    content = models.TextField('상품상세')
    price = models.DecimalField('가격', max_digits=10, decimal_places=2)

    is_sale_period = models.BooleanField('판매기간 설정', default=False)
    started_at = models.DateTimeField('시작일', null=True, default=None)
    finished_at = models.DateTimeField('종료일', null=True, default=None)

    status = models.CharField('승인 상태', max_length=12, default='TEMP_STORAGE', choices=STATUS_CHOICE)
    is_published = models.BooleanField('전시여부', default=True)

    class Meta:
        db_table = 'products'
        ordering = ['-id']
        indexes = [
            models.Index(fields=['code', 'deleted_at']),
            models.Index(fields=['status', 'is_published', 'deleted_at'])
        ]
    
    def __str__(self):
        return f'{self.id}'
    
    def make_code(self):
        self.code = 'PO{:08d}'.format(self.id)
        self.save()

        return self
    
    def approval(self):
        self.status = 'APPROVAL'
        self.save()


class MongoProduct(MongoModel):
    name = 'products'

    def __init__(self, pk: str = None) -> None:
        super().__init__(self.name, pk)

    def __str__(self):
        return self.name