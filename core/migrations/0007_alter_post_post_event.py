# Generated by Django 4.1.3 on 2022-12-05 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_post_post_event'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post_event',
            field=models.CharField(default='other', max_length=40),
        ),
    ]