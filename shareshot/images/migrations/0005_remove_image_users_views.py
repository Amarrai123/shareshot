# Generated by Django 3.2.5 on 2021-11-21 18:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0004_rename_users_likes_image_users_like'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='users_views',
        ),
    ]
