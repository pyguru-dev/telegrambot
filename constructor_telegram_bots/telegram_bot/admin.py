# from django.contrib import admin, messages
# from django.http import HttpRequest
# from django.http.request import HttpRequest
# from django.utils.translation import gettext_lazy as _
# from django.utils import html
# from django.db import models

# from django_json_widget.widgets import JSONEditorWidget

# from .models import TelegramBot, TelegramBotCommand, TelegramBotUser

# from .services import tasks

# from typing import List


# @admin.register(TelegramBot)
# class TelegramBotAdmin(admin.ModelAdmin):
# 	date_hierarchy = 'date_added'
# 	list_filter = ('is_running',)

# 	list_display = (
# 		'id',
# 		'owner',
# 		'show_telegram_bot_username',
# 		'is_private',
# 		'is_running',
# 		'show_telegram_bot_commands_count',
# 		'show_telegram_bot_users_count',
# 		'date_added',
# 	)

# 	fields = ('owner', 'username', 'api_token', 'is_private', 'is_running', 'date_added')

# 	@admin.display(description='@username')
# 	def show_telegram_bot_username(self, telegram_bot: TelegramBot) -> str:
# 		return html.format_html(f'<a href="tg://resolve?domain={telegram_bot.username}">@{telegram_bot.username}</a>')

# 	@admin.display(description=_('Количество команд'))
# 	def show_telegram_bot_commands_count(self, telegram_bot: TelegramBot) -> int:
# 		return telegram_bot.commands.count()

# 	@admin.display(description=_('Количество активаций'))
# 	def show_telegram_bot_users_count(self, telegram_bot: TelegramBot) -> int:
# 		return telegram_bot.users.count()

# 	@admin.action(permissions=['change'], description=_('Включить Telegram бота'))
# 	def start_telegram_bot_button(self, request: HttpRequest, telegram_bots: List[TelegramBot]) -> None:
# 		for telegram_bot in telegram_bots:
# 			if telegram_bot.is_stopped:
# 				tasks.start_telegram_bot.delay(telegram_bot_id=telegram_bot.id)

# 				messages.success(request, f'@{telegram_bot.username} {_("Telegram бот успешно включен.")}')
# 			else:
# 				messages.error(request, f'@{telegram_bot.username} {_("Telegram бот уже включен!")}')

# 	@admin.action(permissions=['change'], description=_('Выключить Telegram бота'))
# 	def stop_telegram_bot_button(self, request: HttpRequest, telegram_bots: List[TelegramBot]) -> None:
# 		for telegram_bot in telegram_bots:
# 			if telegram_bot.is_running:
# 				tasks.stop_telegram_bot.delay(telegram_bot_id=telegram_bot.id)

# 				messages.success(request, f'@{telegram_bot.username} {_("Telegram бот успешно выключен.")}')
# 			else:
# 				messages.error(request, f'@{telegram_bot.username} {_("Telegram бот уже выключен!")}')

# 	actions = [start_telegram_bot_button, stop_telegram_bot_button]

# 	def has_add_permission(self, *args, **kwargs) -> bool:
# 		return False

# 	def has_change_permission(self, *args, **kwargs) -> bool:
# 		return False

# @admin.register(TelegramBotCommand)
# class TelegramBotCommandAdmin(admin.ModelAdmin):
# 	list_display = ('id', 'telegram_bot', 'name')

# 	formfield_overrides = {models.JSONField: {'widget': JSONEditorWidget}}

# 	def has_add_permission(self, *args, **kwargs) -> bool:
# 		return False

# @admin.register(TelegramBotUser)
# class TelegramBotUserAdmin(admin.ModelAdmin):
# 	date_hierarchy = 'date_activated'

# 	list_display = ('id', 'telegram_bot', 'full_name', 'date_activated')

# 	def has_add_permission(self, *args, **kwargs) -> bool:
# 		return False

# 	def has_change_permission(self, *args, **kwargs) -> bool:
# 		return False
