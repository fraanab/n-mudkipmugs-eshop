# Generated by Django 4.1.3 on 2022-12-09 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0007_product_earnings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='earnings',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
