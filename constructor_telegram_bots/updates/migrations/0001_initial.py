# Generated by Django 4.2.1 on 2023-07-01 01:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Update',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='static/images/updates/')),
                ('title', models.CharField(max_length=255, verbose_name='Заголовок')),
                ('title_en', models.CharField(max_length=255, null=True, verbose_name='Заголовок')),
                ('title_uk', models.CharField(max_length=255, null=True, verbose_name='Заголовок')),
                ('title_ru', models.CharField(max_length=255, null=True, verbose_name='Заголовок')),
                ('description', models.TextField(verbose_name='Описание')),
                ('description_en', models.TextField(null=True, verbose_name='Описание')),
                ('description_uk', models.TextField(null=True, verbose_name='Описание')),
                ('description_ru', models.TextField(null=True, verbose_name='Описание')),
                ('views', models.BigIntegerField(default=0, verbose_name='Просмотры')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')),
            ],
            options={
                'verbose_name': 'Обновление',
                'verbose_name_plural': 'Обновления',
                'db_table': 'update',
            },
        ),
        migrations.CreateModel(
            name='UpdateLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('update', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='updates.update')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'update_like',
            },
        ),
        migrations.CreateModel(
            name='UpdateComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('update', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='updates.update')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'update_comment',
            },
        ),
    ]
