# Generated by Django 2.2.5 on 2020-12-06 06:58

import account.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_customer', models.BooleanField(default=False)),
                ('is_shop', models.BooleanField(default=False)),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', account.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='user')),
                ('first_name', models.CharField(max_length=150, verbose_name='名前')),
                ('last_name', models.CharField(max_length=150, verbose_name='苗字')),
                ('gender', models.IntegerField(blank=True, choices=[(1, '男性'), (2, '女性'), (3, 'その他')], null=True, verbose_name='性別')),
                ('age', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)], verbose_name='年齢')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='user')),
                ('shop_name', models.CharField(max_length=150, verbose_name='店舗名')),
                ('has_point', models.BooleanField(default=False, help_text='ユーザがポイントカードを作成したときにそのポイントカードがポイントカード機能を使用するか', verbose_name='ポイント機能を使用する')),
                ('has_stamp', models.BooleanField(default=False, help_text='ユーザがポイントカードを作成したときにそのポイントカードがポイントカード機能を使用するか', verbose_name='スタンプ機能を使用する')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PointCard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('has_point', models.BooleanField(default=False)),
                ('has_stamp', models.BooleanField(default=False)),
                ('point', models.IntegerField(blank=True, null=True)),
                ('number_of_stamps', models.IntegerField(blank=True, null=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Customer', verbose_name='customer')),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Shop', verbose_name='shop')),
            ],
            options={
                'verbose_name': 'point card',
                'verbose_name_plural': 'point cards',
            },
        ),
    ]
