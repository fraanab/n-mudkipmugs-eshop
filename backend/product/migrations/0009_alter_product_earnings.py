# Generated by Django 4.1.3 on 2022-12-09 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_alter_product_earnings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='earnings',
            field=models.IntegerField(default=0),
        ),
    ]
