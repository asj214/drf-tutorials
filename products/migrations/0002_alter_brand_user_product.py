# Generated by Django 4.0.1 on 2022-01-14 13:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='user',
            field=models.ForeignKey(db_constraint=False, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='brands', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, default=None, max_length=30, null=True, verbose_name='상품 코드 Ex. PR00000001')),
                ('type', models.CharField(choices=[('GENERAL', '일반상품'), ('OPTION', '옵션상품'), ('PACKAGE', '패키지상품')], max_length=10, verbose_name='상품 유형')),
                ('user', models.ForeignKey(db_constraint=False, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='products', to=settings.AUTH_USER_MODEL)),
                ('name', models.CharField(max_length=200, verbose_name='상품명')),
                ('brand', models.ForeignKey(db_constraint=False, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='products', to='products.brand')),
                ('content', models.TextField(verbose_name='상품상세')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='가격')),
                ('is_sale_period', models.BooleanField(default=False, verbose_name='판매기간 설정')),
                ('started_at', models.DateTimeField(default=None, null=True, verbose_name='시작일')),
                ('finished_at', models.DateTimeField(default=None, null=True, verbose_name='종료일')),
                ('is_published', models.BooleanField(default=True, verbose_name='전시여부')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='등록일')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정일')),
                ('deleted_at', models.DateTimeField(default=None, null=True, verbose_name='삭제일')),
            ],
            options={
                'db_table': 'products',
                'ordering': ['-id'],
            },
        ),
    ]
