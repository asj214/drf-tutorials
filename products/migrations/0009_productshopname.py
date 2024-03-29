# Generated by Django 4.0.1 on 2022-01-18 06:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('products', '0008_delete_productapproval'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductShopName',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_id', models.PositiveIntegerField(blank=True, db_column='content_id', default=None, null=True)),
                ('content_type', models.ForeignKey(db_constraint=False, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.contenttype')),
                ('code', models.CharField(max_length=200)),
                ('value', models.CharField(max_length=200)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='가격')),
                ('started_at', models.DateTimeField(default=None, null=True, verbose_name='시작일')),
                ('finished_at', models.DateTimeField(default=None, null=True, verbose_name='종료일')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='등록일')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='수정일')),
            ],
            options={
                'db_table': 'product_shop_names',
                'ordering': ['-id'],
            },
        ),
    ]
