# Generated by Django 2.1.4 on 2018-12-17 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_post_liked_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='like',
            field=models.SmallIntegerField(default=0),
        ),
    ]
