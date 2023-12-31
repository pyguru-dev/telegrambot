# Generated by Django 4.2.3 on 2023-09-22 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telegram_bot', '0017_alter_telegrambotcommand_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='telegrambotcommandcommand',
            old_name='show_in_menu',
            new_name='is_show_in_menu',
        ),
        migrations.RenameField(
            model_name='telegrambotcommandcommand',
            old_name='command',
            new_name='text',
        ),
        migrations.AddField(
            model_name='telegrambotcommandcommand',
            name='description',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='telegrambot',
            name='is_private',
            field=models.BooleanField(default=False, verbose_name='Приватный'),
        ),
        migrations.AlterField(
            model_name='telegrambotcommandapirequest',
            name='url',
            field=models.TextField(max_length=2048, verbose_name='URL-адрес'),
        ),
    ]
