from django.db import models

from django.utils.translation import gettext_lazy as _

from django.core.exceptions import ObjectDoesNotExist

from user.models import User
from telegram_bot.managers import (
	TelegramBotManager,
	TelegramBotCommandManager, TelegramBotCommandKeyboardManager
)

from django.conf import settings
from typing import Union
import pytz


class TelegramBot(models.Model):
	owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='telegram_bots', null=True, verbose_name=_('Владелец'))

	username = models.CharField('@username', max_length=32, unique=True)
	api_token = models.CharField(max_length=50, unique=True)
	is_private = models.BooleanField(_('Приватный'))
	is_running = models.BooleanField(_('Включён'), default=False)
	is_stopped = models.BooleanField(default=True)
	_date_added = models.DateTimeField(_('Дата добавления'), auto_now_add=True)

	diagram_current_scale = models.FloatField(default=1.0)

	objects = TelegramBotManager()

	class Meta:
		db_table = 'telegram_bot'

		verbose_name = _('Telegram бота')
		verbose_name_plural = _('Telegram боты')

	@property
	def date_added(self) -> str:
		return self._date_added.astimezone(
			pytz.timezone(settings.TIME_ZONE)
		).strftime('%d.%m.%Y - %H:%M:%S')

	def get_commands_as_dict(self) -> list:
		return [command.to_dict() for command in self.commands.all()]

	def get_users_as_dict(self) -> list:
		return [user.to_dict() for user in self.users.all()]

	def to_dict(self) -> dict:
		return {
			'id': self.id,
			'username': self.username,
			'api_token': self.api_token,
			'is_running': self.is_running,
			'is_stopped': self.is_stopped,
			'commands_count': self.commands.count(),
			'users_count': self.users.count(),
			'date_added': self.date_added,
		}
	
	def __str__(self) -> str:
		return f'@{self.username} {_("Telegram бот")}'


class TelegramBotCommand(models.Model):
	telegram_bot = models.ForeignKey(TelegramBot, on_delete=models.CASCADE, related_name='commands', null=True)

	name = models.CharField(max_length=255)
	command = models.CharField(max_length=32, null=True)
	image = models.ImageField(upload_to='static/images/commands/', null=True)
	message_text = models.TextField(max_length=4096)
	api_request = models.JSONField(null=True)

	x =	models.IntegerField(default=0)
	y = models.IntegerField(default=0)

	objects = TelegramBotCommandManager()

	class Meta:
		db_table = 'telegram_bot_command'

	def get_keyboard_as_dict(self) -> Union[dict, None]:
		keyboard: Union['TelegramBotCommandKeyboard', None] = self.get_keyboard()

		if keyboard is not None:
			return keyboard.to_dict()

		return None
		
	def get_keyboard(self) -> Union['TelegramBotCommandKeyboard', None]:
		try:
			return self.keyboard
		except ObjectDoesNotExist:
			return None

	def to_dict(self) -> dict:
		return {
			'id': self.id,
			'name': self.name,
			'command': self.command,
			'image': str(self.image),
			'message_text': self.message_text,
			'keyboard': self.get_keyboard_as_dict(),
			'api_request': self.api_request,

			'x': self.x,
			'y': self.y,
		}
	
	def delete(self) -> None:
		self.image.delete(save=False)
		return super().delete()


class TelegramBotCommandKeyboard(models.Model):
	telegram_bot_command = models.OneToOneField(TelegramBotCommand, on_delete=models.CASCADE, related_name='keyboard', null=True)

	type = models.CharField(max_length=7, choices=(('default', 'Default',), ('inline', 'Inline',),), default='default')

	objects = TelegramBotCommandKeyboardManager()

	class Meta:
		db_table = 'telegram_bot_command_keyboard'

	def get_buttons_as_dict(self) -> list:
		return [button.to_dict() for button in self.buttons.all()]

	def to_dict(self) -> dict:
		return {
			'type': self.type,
			'buttons': self.get_buttons_as_dict(),
		}


class TelegramBotCommandKeyboardButton(models.Model):
	telegram_bot_command_keyboard = models.ForeignKey(TelegramBotCommandKeyboard, on_delete=models.CASCADE, related_name='buttons', null=True)

	row = models.IntegerField(null=True)

	text = models.TextField(max_length=4096)
	url = models.TextField(max_length=2048, null=True)

	telegram_bot_command = models.ForeignKey(TelegramBotCommand, on_delete=models.SET_NULL, null=True)
	start_diagram_connector = models.TextField(null=True)
	end_diagram_connector = models.TextField(null=True)

	class Meta:
		db_table = 'telegram_bot_command_keyboard_button'

	def to_dict(self) -> dict:
		return {
			'id': self.id,

			'row': self.row,

			'text': self.text,
			'url': self.url,

			'telegram_bot_command_id': self.telegram_bot_command.id if self.telegram_bot_command is not None else None,
			'start_diagram_connector': self.start_diagram_connector,
			'end_diagram_connector' : self.end_diagram_connector,
		}


class TelegramBotUser(models.Model):
	telegram_bot = models.ForeignKey(TelegramBot, on_delete=models.CASCADE, related_name='users', null=True)

	user_id = models.BigIntegerField()
	full_name = models.CharField(max_length=129, null=True)
	is_allowed = models.BooleanField(default=False)
	_date_activated = models.DateTimeField(auto_now_add=True)

	class Meta:
		db_table = 'telegram_bot_user'

	@property
	def date_activated(self) -> str:
		return self._date_activated.astimezone(
			pytz.timezone(settings.TIME_ZONE)
		).strftime('%d.%m.%Y - %H:%M:%S')
	
	def to_dict(self) -> dict:
		return {
			'id': self.id,
			'user_id': self.user_id,
			'full_name': self.full_name,
			'is_allowed': self.is_allowed,
			'date_activated': self.date_activated,
		}
