# Generated by Django 2.2.5 on 2020-10-21 15:04

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20201020_0545'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='age',
            field=models.IntegerField(blank=True, null=True, unique=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)], verbose_name=' age '),
        ),
        migrations.AlterField(
            model_name='user',
            name='sex',
            field=models.IntegerField(blank=True, choices=[(1, '男性'), (2, '女性'), (3, 'その他')], null=True, verbose_name=' sex '),
        ),
    ]
