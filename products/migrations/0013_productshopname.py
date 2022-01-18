# Generated by Django 4.0.1 on 2022-01-18 07:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_delete_productshopname'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductShopName',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='등록일')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정일')),
                ('code', models.CharField(max_length=200)),
                ('value', models.CharField(max_length=200)),
                ('is_sale_period', models.BooleanField(default=False, verbose_name='판매기간 설정')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='가격')),
                ('started_at', models.DateTimeField(default=None, null=True, verbose_name='시작일')),
                ('finished_at', models.DateTimeField(default=None, null=True, verbose_name='종료일')),
                ('product', models.ForeignKey(db_constraint=False, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='shops', to='products.product')),
            ],
            options={
                'db_table': 'product_shop_names',
                'ordering': ['-id'],
            },
        ),
    ]
