# Generated by Django 2.2.16 on 2022-05-15 16:35

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ('name',), 'verbose_name': 'категория', 'verbose_name_plural': 'категории'},
        ),
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ('pub_date',)},
        ),
        migrations.AlterModelOptions(
            name='genre',
            options={'ordering': ('name',), 'verbose_name': 'жанр', 'verbose_name_plural': 'жанры'},
        ),
        migrations.AlterModelOptions(
            name='review',
            options={'ordering': ('pub_date',), 'verbose_name': 'отзыв', 'verbose_name_plural': 'отзывы'},
        ),
        migrations.AlterModelOptions(
            name='title',
            options={'ordering': ('name',), 'verbose_name': 'произведение', 'verbose_name_plural': 'произведения'},
        ),
        migrations.AlterField(
            model_name='review',
            name='score',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)], verbose_name='оценка'),
        ),
        migrations.AlterField(
            model_name='user',
            name='bio',
            field=models.TextField(blank=True, default='пусто', max_length=600, verbose_name='Биография'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(blank=True, choices=[('user', 'Пользователь'), ('moderator', 'Модератор'), ('admin', 'Администратор')], default='user', max_length=30, verbose_name='Роль'),
        ),
    ]
