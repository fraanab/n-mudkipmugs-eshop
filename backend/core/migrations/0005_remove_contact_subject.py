# Generated by Django 4.1.3 on 2022-12-07 19:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_contact_subject'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contact',
            name='subject',
        ),
    ]
