from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from django.template import defaultfilters as filters
from django.core.files.uploadedfile import InMemoryUploadedFile

from user.models import User
from telegram_bot.managers import (
	TelegramBotManager,
	TelegramBotCommandManager, TelegramBotCommandKeyboardManager
)

from typing import Union


class TelegramBot(models.Model):
	owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='telegram_bots', null=True, verbose_name=_('Владелец'))
	username = models.CharField('@username', max_length=32, unique=True)
	api_token = models.CharField(max_length=50, unique=True)
	is_private = models.BooleanField(_('Приватный'))
	is_running = models.BooleanField(_('Включён'), default=False)
	is_stopped = models.BooleanField(default=True)
	date_added = models.DateTimeField(_('Дата добавления'), auto_now_add=True)

	diagram_current_scale = models.FloatField(default=1.0)

	objects = TelegramBotManager()

	class Meta:
		db_table = 'telegram_bot'

		verbose_name = _('Telegram бота')
		verbose_name_plural = _('Telegram боты')

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
			'date_added': f'{filters.date(self.date_added)} {filters.time(self.date_added)}',
		}

	def __str__(self) -> str:
		return f'@{self.username}'


class TelegramBotCommand(models.Model):
	telegram_bot = models.ForeignKey(TelegramBot, on_delete=models.CASCADE, related_name='commands', null=True, verbose_name=_('Telegram бот'))
	name = models.CharField(_('Название'), max_length=255)
	command = models.CharField(_('Команда'), max_length=32, blank=True, null=True)
	image = models.ImageField(upload_to='static/images/commands/', blank=True, null=True)
	message_text = models.TextField(_('Текст сообщения'), max_length=4096)
	api_request = models.JSONField(_('API-запрос'), blank=True, null=True)
	database_record = models.TextField(_('Запись в базу данных'), blank=True, null=True)

	x =	models.IntegerField(_('Координата X'), default=0)
	y = models.IntegerField(_('Координата Y'), default=0)

	objects = TelegramBotCommandManager()

	class Meta:
		db_table = 'telegram_bot_command'

		verbose_name = _('Команда Telegram бота')
		verbose_name_plural = _('Команды Telegram ботов')

	def get_keyboard(self) -> Union['TelegramBotCommandKeyboard', None]:
		try:
			return self.keyboard
		except ObjectDoesNotExist:
			return None

	def get_keyboard_as_dict(self) -> Union[dict, None]:
		keyboard: Union['TelegramBotCommandKeyboard', None] = self.get_keyboard()
		return keyboard.to_dict() if keyboard else None

	def to_dict(self) -> dict:
		return {
			'id': self.id,
			'name': self.name,
			'command': self.command,
			'image': str(self.image),
			'message_text': self.message_text,
			'keyboard': self.get_keyboard_as_dict(),
			'api_request': self.api_request,
			'database_record': self.database_record,
			'x': self.x,
			'y': self.y,
		}

	def update(
		self,
	    telegram_bot_command: 'TelegramBotCommand',
		name: str,
		message_text: str,
		command: Union[str, None] = None,
		image: Union[InMemoryUploadedFile, str, None] = None,
		keyboard: Union[dict, None] = None,
		api_request: Union[dict, None] = None,
		database_record: Union[str, None] = None
	):
		telegram_bot_command.name = name
		telegram_bot_command.command = command
		telegram_bot_command.message_text = message_text
		telegram_bot_command.api_request = api_request
		telegram_bot_command.database_record = database_record

		if image:
			if isinstance(image, InMemoryUploadedFile) or image == 'null' and str(telegram_bot_command.image) != '':
				telegram_bot_command.image.delete(save=False)

				if isinstance(image, InMemoryUploadedFile):
					telegram_bot_command.image = image

		telegram_bot_command_keyboard: TelegramBotCommandKeyboard = telegram_bot_command.get_keyboard()

		if keyboard:
			if telegram_bot_command_keyboard:
				telegram_bot_command_keyboard.type = keyboard['type']
				telegram_bot_command_keyboard.save()

				buttons_id = []

				for button in keyboard['buttons']:
					if not button['id']:
						button_: TelegramBotCommandKeyboardButton = TelegramBotCommandKeyboardButton.objects.create(
							telegram_bot_command_keyboard=telegram_bot_command_keyboard,
							**button
						)
					else:
						button_id = int(button['id'])

						is_finded_button = False

						for button_ in telegram_bot_command_keyboard.buttons.all():
							if button_id == button_.id:
								is_finded_button = True
								break

						if is_finded_button:
							button_: TelegramBotCommandKeyboardButton = telegram_bot_command_keyboard.buttons.get(id=button_id)
							button_.row = button['row']
							button_.text = button['text']
							button_.url = button['url']
							button_.save()
						else:
							button_: TelegramBotCommandKeyboardButton = TelegramBotCommandKeyboardButton.objects.create(
								telegram_bot_command_keyboard=telegram_bot_command_keyboard,
								**button
							)

					buttons_id.append(button_.id)

				for button in telegram_bot_command_keyboard.buttons.all():
					if button.id not in buttons_id:
						button.delete()
			else:
				TelegramBotCommandKeyboard.objects.create(
					telegram_bot_command=telegram_bot_command,
					type=keyboard['type'],
					buttons=keyboard['buttons']
				)
		else:
			if telegram_bot_command_keyboard:
				telegram_bot_command_keyboard.delete()

		telegram_bot_command.save()

	def delete(self) -> None:
		self.image.delete(save=False)
		return super().delete()

	def __str__(self) -> str:
		return f'Команда {self.name} @{self.telegram_bot.username} {_("Telegram бота")}'


class TelegramBotCommandKeyboard(models.Model):
	telegram_bot_command = models.OneToOneField(TelegramBotCommand, on_delete=models.CASCADE, related_name='keyboard', null=True)
	type = models.CharField(max_length=7, choices=(('default', 'Default'), ('inline', 'Inline')), default='default')

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

	def get_command(self) -> Union[TelegramBotCommand, None]:
		return self.telegram_bot_command

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
	telegram_bot = models.ForeignKey(TelegramBot, on_delete=models.CASCADE, related_name='users', verbose_name=_('Telegram бот'), null=True)
	user_id = models.BigIntegerField(_('Telegram ID пользователя'))
	full_name = models.CharField(_('Полное имя пользователя'), max_length=129, null=True)
	is_allowed = models.BooleanField(_('Разрешён'), default=False)
	date_activated = models.DateTimeField(_('Дата активации'), auto_now_add=True)

	class Meta:
		db_table = 'telegram_bot_user'

		verbose_name = _('Пользователя Telegram бота')
		verbose_name_plural = _('Пользователи Telegram ботов')

	def to_dict(self) -> dict:
		return {
			'id': self.id,
			'user_id': self.user_id,
			'full_name': self.full_name,
			'is_allowed': self.is_allowed,
			'date_activated': f'{filters.date(self.date_activated)} {filters.time(self.date_activated)}',
		}

	def __str__(self) -> str:
		return self.full_name
