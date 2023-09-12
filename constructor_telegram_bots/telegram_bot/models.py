from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from django.template import defaultfilters as filters
from django.core.files.uploadedfile import InMemoryUploadedFile

from user.models import User

from .services import database_telegram_bot
from .functions import check_telegram_bot_api_token

from asgiref.sync import sync_to_async
from typing import Optional, Union


class TelegramBotManager(models.Manager):
	def create(self, owner: User, api_token: str, is_private: bool = False, **extra_fields) -> 'TelegramBot':
		username: str = check_telegram_bot_api_token(api_token)

		return super().create(
			owner=owner,
			username=username,
			api_token=api_token,
			is_private=is_private,
			**extra_fields
		)

class TelegramBot(models.Model):
	owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='telegram_bots', verbose_name=_('Владелец'), null=True)
	username = models.CharField('@username', max_length=32, unique=True)
	api_token = models.CharField(_('API-токен'), max_length=50, unique=True)
	is_private = models.BooleanField(_('Приватный'))
	is_running = models.BooleanField(_('Включён'), default=False)
	is_stopped = models.BooleanField(default=True)
	added_date = models.DateTimeField(_('Дата добавления'), auto_now_add=True)

	diagram_current_scale = models.FloatField(default=1.0)

	objects = TelegramBotManager()

	class Meta:
		db_table = 'telegram_bot'

		verbose_name = _('Telegram бота')
		verbose_name_plural = _('Telegram боты')

	def get_commands_as_dict(self, escape: bool = False) -> list:
		return [command.to_dict(escape=escape) for command in self.commands.all()]

	def get_users_as_dict(self) -> list:
		return [user.to_dict() for user in self.users.all()]

	def to_dict(self) -> dict:
		return {
			'id': self.id,
			'username': self.username,
			'api_token': self.api_token,
			'is_private': self.is_private,
			'is_running': self.is_running,
			'is_stopped': self.is_stopped,
			'commands_count': self.commands.count(),
			'users_count': self.users.count(),
			'added_date': f'{filters.date(self.added_date)} {filters.time(self.added_date)}',
		}

	def delete(self) -> None:
		database_telegram_bot.delete_collection(self)
		super().delete()

	def __str__(self) -> str:
		return f'@{self.username}'

class TelegramBotCommandManager(models.Manager):
	def create(
		self,
		telegram_bot: TelegramBot,
		name: str,
		command: Optional[dict],
		image: Optional[InMemoryUploadedFile],
		message_text: dict,
		keyboard: Optional[dict],
		api_request: Optional[dict],
		database_record: Optional[dict],
	) -> 'TelegramBotCommand':
		telegram_bot_command: TelegramBotCommand = super().create(
			telegram_bot=telegram_bot,
			name=name,
			image=image if isinstance(image, InMemoryUploadedFile) else None,
			database_record=database_record
		)

		if command:
			TelegramBotCommandCommand.objects.create(
				telegram_bot_command=telegram_bot_command,
				command=command['command'],
				show_in_menu=command['show_in_menu']
			)

		TelegramBotCommandMessageText.objects.create(
			telegram_bot_command=telegram_bot_command,
			mode=message_text['mode'],
			text=message_text['text']
		)

		if keyboard:
			TelegramBotCommandKeyboard.objects.create(
				telegram_bot_command=telegram_bot_command,
				mode=keyboard['mode'],
				buttons=keyboard['buttons']
			)

		if api_request:
			TelegramBotCommandApiRequest.objects.create(
				telegram_bot_command=telegram_bot_command,
				url=api_request['url'],
				method=api_request['method'],
				headers=api_request['headers'],
				data=api_request['data']
			)

		return telegram_bot_command

	async def acreate(self, *args, **kwargs) -> 'TelegramBotCommand':
		return await sync_to_async(self.create)(*args, **kwargs)

class TelegramBotCommand(models.Model):
	telegram_bot = models.ForeignKey(TelegramBot, on_delete=models.CASCADE, related_name='commands', null=True, verbose_name=_('Telegram бот'))
	name = models.CharField(_('Название'), max_length=255)
	image = models.ImageField(_('Изображение'), upload_to='static/images/commands/', blank=True, null=True)
	database_record = models.JSONField(_('Запись в базу данных'), blank=True, null=True)

	x =	models.IntegerField(_('Координата X'), default=0)
	y = models.IntegerField(_('Координата Y'), default=0)

	objects = TelegramBotCommandManager()

	class Meta:
		db_table = 'telegram_bot_command'

		verbose_name = _('Команда')
		verbose_name_plural = _('Команды')

	def get_command(self) -> Optional['TelegramBotCommandCommand']:
		try:
			return self.command
		except ObjectDoesNotExist:
			return None

	async def aget_command(self) -> Optional['TelegramBotCommandCommand']:
		return await sync_to_async(self.get_command)()

	def get_message_text(self) -> Optional['TelegramBotCommandMessageText']:
		try:
			return self.message_text
		except ObjectDoesNotExist:
			return None

	async def aget_message_text(self) -> Optional['TelegramBotCommandMessageText']:
		return await sync_to_async(self.get_message_text)()

	def get_keyboard(self) -> Optional['TelegramBotCommandKeyboard']:
		try:
			return self.keyboard
		except ObjectDoesNotExist:
			return None

	async def aget_keyboard(self) -> Optional['TelegramBotCommandKeyboard']:
		return await sync_to_async(self.get_keyboard)()

	def get_keyboard_as_dict(self, escape: bool = False) -> Optional[dict]:
		keyboard: Optional[TelegramBotCommandKeyboard] = self.get_keyboard()
		return keyboard.to_dict(escape=escape) if keyboard else None

	def get_api_request(self) -> Optional['TelegramBotCommandApiRequest']:
		try:
			return self.api_request
		except ObjectDoesNotExist:
			return None

	async def aget_api_request(self) -> Optional['TelegramBotCommandApiRequest']:
		return await sync_to_async(self.get_api_request)()

	def to_dict(self, escape: bool = False) -> dict:
		command: Optional[TelegramBotCommandCommand] = self.get_command()
		api_request: Optional[TelegramBotCommandApiRequest] = self.get_api_request()

		return {
			'id': self.id,
			'name': filters.escape(self.name) if escape else self.name,
			'command': command.to_dict() if command else None,
			'image': str(self.image),
			'message_text': self.message_text.to_dict(escape=escape),
			'keyboard': self.get_keyboard_as_dict(escape=escape),
			'api_request': api_request.to_dict() if api_request else None,
			'database_record': self.database_record,

			'x': self.x,
			'y': self.y,
		}

	def update(self, *,
		name: str,
		command: Optional[dict],
		image: Union[InMemoryUploadedFile, str, None],
		message_text: dict,
		keyboard: Optional[dict],
		api_request: Optional[dict],
		database_record: Optional[dict],
	):
		self.name = name
		self.database_record = database_record

		telegram_bot_command_command: Optional[TelegramBotCommandCommand] = self.get_command()

		if telegram_bot_command_command:
			if command:
				telegram_bot_command_command.command = command['command']
				telegram_bot_command_command.show_in_menu = command['show_in_menu']
			else:
				telegram_bot_command_command.delete()

		if isinstance(image, InMemoryUploadedFile) or image == 'null' and str(self.image) != '':
			self.image.delete(save=False)

			if isinstance(image, InMemoryUploadedFile):
				self.image = image

		self.message_text.mode = message_text['mode']
		self.message_text.text = message_text['text']

		telegram_bot_command_keyboard: Optional[TelegramBotCommandKeyboard] = self.get_keyboard()

		if telegram_bot_command_keyboard:
			if keyboard:
				telegram_bot_command_keyboard.mode = keyboard['mode']
				telegram_bot_command_keyboard.save()

				buttons_id = []

				for button in keyboard['buttons']:
					is_finded_button = False

					if button['id']:
						button_id = int(button['id'])

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
							row = button['row'],
							text = button['text'],
							url = button['url']
						)

					buttons_id.append(button_.id)

				for button in telegram_bot_command_keyboard.buttons.all():
					if button.id not in buttons_id:
						button.delete()
			else:
				telegram_bot_command_keyboard.delete()
		else:
			TelegramBotCommandKeyboard.objects.create(
				telegram_bot_command=self,
				type=keyboard['mode'],
				buttons=keyboard['buttons']
			)

		telegram_bot_command_api_request: Optional[TelegramBotCommandApiRequest] = self.get_api_request()

		if telegram_bot_command_api_request:
			if api_request:
				telegram_bot_command_api_request.url = api_request['url']
				telegram_bot_command_api_request.method = api_request['method']
				telegram_bot_command_api_request.headers = api_request['headers']
				telegram_bot_command_api_request.data = api_request['data']
			else:
				telegram_bot_command_api_request.delete()

		self.save()

	def delete(self) -> None:
		self.image.delete(save=False)
		return super().delete()

	def __str__(self) -> str:
		return self.name

class TelegramBotCommandCommand(models.Model):
	telegram_bot_command = models.OneToOneField(TelegramBotCommand, on_delete=models.CASCADE, related_name='command')
	command = models.CharField(_('Команда'), max_length=32)
	show_in_menu = models.BooleanField(_('Отображать в меню'), default=False)

	class Meta:
		db_table = 'telegram_bot_command_command'

	def to_dict(self) -> dict:
		return {
			'command': self.command,
			'show_in_menu': self.show_in_menu,
		}

class TelegramBotCommandMessageText(models.Model):
	telegram_bot_command = models.OneToOneField(TelegramBotCommand, on_delete=models.CASCADE, related_name='message_text')
	mode = models.CharField(_('Режим'), max_length=8, choices=(
		('default', _('Обычный')),
		('markdown', 'Markdown'),
		('html', 'HTML'),
	), default='default')
	text = models.TextField(_('Текст'), max_length=4096)

	class Meta:
		db_table = 'telegram_bot_command_message_text'

	def to_dict(self, escape: bool = False) -> dict:
		return {
			'mode': self.mode,
			'text': filters.escape(self.text) if escape else self.text,
		}

class TelegramBotCommandKeyboardManager(models.Manager):
	def create(self, *,
		telegram_bot_command: TelegramBotCommand,
		mode: str,
		buttons: list
	) -> 'TelegramBotCommandKeyboard':
		telegram_bot_command_keyboard: TelegramBotCommandKeyboard = super().create(telegram_bot_command=telegram_bot_command, mode=mode)

		for button in buttons:
			TelegramBotCommandKeyboardButton.objects.create(
				telegram_bot_command_keyboard=telegram_bot_command_keyboard,
				row=button['row'],
				text=button['text'],
				url=button['url']
			)

		return telegram_bot_command_keyboard

class TelegramBotCommandKeyboard(models.Model):
	telegram_bot_command = models.OneToOneField(TelegramBotCommand, on_delete=models.CASCADE, related_name='keyboard', null=True)
	mode = models.CharField(_('Режим'), max_length=7, choices=(
		('default', _('Обычный')),
		('inline', _('Встроенный')),
		('payment', _('Платёжный')),
   	), default='default')

	objects = TelegramBotCommandKeyboardManager()

	class Meta:
		db_table = 'telegram_bot_command_keyboard'

	def get_buttons_as_dict(self, escape: bool = False) -> list:
		return [button.to_dict(escape=escape) for button in self.buttons.all()]

	def to_dict(self, escape: bool = False) -> dict:
		return {
			'mode': self.mode,
			'buttons': self.get_buttons_as_dict(escape=escape),
		}

class TelegramBotCommandKeyboardButton(models.Model):
	telegram_bot_command_keyboard = models.ForeignKey(TelegramBotCommandKeyboard, on_delete=models.CASCADE, related_name='buttons', null=True)
	row = models.IntegerField(_('Ряд'), blank=True, null=True)
	text = models.TextField(_('Текст'), max_length=4096)
	url = models.TextField(_('URL-адрес'), max_length=2048, blank=True, null=True)

	telegram_bot_command = models.ForeignKey(TelegramBotCommand, on_delete=models.SET_NULL, blank=True, null=True)

	start_diagram_connector = models.TextField(blank=True, null=True)
	end_diagram_connector = models.TextField(blank=True, null=True)

	class Meta:
		db_table = 'telegram_bot_command_keyboard_button'
		ordering = ['id']

	def get_telegram_bot_command(self) -> Optional[TelegramBotCommand]:
		return self.telegram_bot_command

	async def aget_telegram_bot_command(self) -> Optional[TelegramBotCommand]:
		return await sync_to_async(self.get_telegram_bot_command)()

	def to_dict(self, escape: bool = False) -> dict:
		return {
			'id': self.id,
			'row': self.row,
			'text': filters.escape(self.text) if escape else self.text,
			'url': self.url,

			'telegram_bot_command_id': self.telegram_bot_command.id if self.telegram_bot_command else None,

			'start_diagram_connector': self.start_diagram_connector,
			'end_diagram_connector' : self.end_diagram_connector,
		}

class TelegramBotCommandApiRequest(models.Model):
	telegram_bot_command = models.OneToOneField(TelegramBotCommand, on_delete=models.CASCADE, related_name='api_request')
	url = models.URLField(_('URL-адрес'))
	method = models.CharField(_('Метод'), max_length=6, choices=(
		('get', 'GET'),
		('post', 'POST'),
		('put', 'PUT'),
		('patch', 'PATCH'),
		('delete', 'DELETE'),
	), default='get')
	headers = models.JSONField(_('Заголовки'), blank=True, null=True)
	data = models.JSONField(_('Данные'), blank=True, null=True)

	class Meta:
		db_table = 'telegram_bot_command_api_request'

	def to_dict(self) -> dict:
		return {
			'url': self.url,
			'method': self.method,
			'headers': self.headers,
			'data': self.data,
		}

class TelegramBotUser(models.Model):
	telegram_bot = models.ForeignKey(TelegramBot, on_delete=models.CASCADE, related_name='users', verbose_name=_('Telegram бот'), null=True)
	user_id = models.BigIntegerField('Telegram ID')
	full_name = models.CharField(_('Полное имя'), max_length=129, null=True)
	is_allowed = models.BooleanField(_('Разрешён'), default=False)
	activated_date = models.DateTimeField(_('Дата активации'), auto_now_add=True)

	class Meta:
		db_table = 'telegram_bot_user'

		verbose_name = _('Пользователя')
		verbose_name_plural = _('Пользователи')

	def to_dict(self) -> dict:
		return {
			'id': self.id,
			'user_id': self.user_id,
			'full_name': self.full_name,
			'is_allowed': self.is_allowed,
			'activated_date': f'{filters.date(self.activated_date)} {filters.time(self.activated_date)}',
		}

	def __str__(self) -> str:
		return self.full_name
