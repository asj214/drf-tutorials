# Generated by Django 4.0.1 on 2022-01-14 13:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_alter_brand_user_product'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Product',
        ),
    ]