# Generated by Django 4.0 on 2024-04-16 11:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_friends'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Friends',
        ),
    ]
