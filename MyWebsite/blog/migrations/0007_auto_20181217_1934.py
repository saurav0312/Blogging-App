# Generated by Django 2.1.4 on 2018-12-17 14:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20181217_1930'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='like',
        ),
        migrations.DeleteModel(
            name='Like',
        ),
    ]
