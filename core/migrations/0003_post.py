# Generated by Django 4.1.3 on 2022-12-04 07:46

import datetime
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_profile_bio'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('user', models.CharField(max_length=30)),
                ('image', models.ImageField(default='defualt.jpg', upload_to='post_images')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(max_length=1000)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('likes', models.IntegerField(default=0)),
            ],
        ),
    ]