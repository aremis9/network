# Generated by Django 3.2.6 on 2021-08-10 07:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_follow_post'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='likes',
        ),
    ]