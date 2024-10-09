# Generated by Django 5.1.1 on 2024-10-08 06:53

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_blog_likes_blog_rating_comment'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='dislikes',
            field=models.ManyToManyField(blank=True, related_name='disliked_blogs', to=settings.AUTH_USER_MODEL),
        ),
    ]