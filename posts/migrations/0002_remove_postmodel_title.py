# Generated by Django 4.0 on 2024-04-14 09:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='postmodel',
            name='title',
        ),
    ]
