# Generated by Django 4.1.3 on 2022-12-08 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_alter_category_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='ordered_times',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
