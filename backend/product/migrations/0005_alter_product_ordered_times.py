# Generated by Django 4.1.3 on 2022-12-08 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_product_ordered_times'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='ordered_times',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
