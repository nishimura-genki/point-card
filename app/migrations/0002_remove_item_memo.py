# Generated by Django 2.2.5 on 2020-10-15 06:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='memo',
        ),
    ]
