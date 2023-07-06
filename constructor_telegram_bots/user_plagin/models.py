from django.db import models
from django.utils.translation import gettext_lazy as _

from user.models import User
from telegram_bot.models import TelegramBot

from constructor_telegram_bots.functions import generate_random_string


class UserPlagin(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Пользователь'))
	telegram_bot = models.ForeignKey(TelegramBot, on_delete=models.CASCADE, verbose_name=_('Telegram бот'))
	name = models.CharField(_('Название'), max_length=255)
	code = models.TextField(_('Код'))
	is_checked = models.BooleanField(_('Проверен'))
	date_added = models.DateTimeField(_('Дата добавления'), auto_now_add=True)

	class Meta:
		db_table = 'user_plagin'

		verbose_name = _('Плагин пользователя')
		verbose_name_plural = _('Плагины пользователей')

	def __str__(self) -> str:
		return self.name


class UserPlaginLog(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Пользователь'))
	telegram_bot = models.ForeignKey(TelegramBot, on_delete=models.CASCADE, verbose_name=_('Telegram бот'))
	plagin = models.ForeignKey(UserPlagin, on_delete=models.CASCADE, verbose_name=_('Плагин'))
	message = models.TextField(_('Сообщение'))
	level = models.CharField(_('Уровень'), max_length=7, choices=(('info', 'Info'), ('success', 'Success'), ('danger', 'Danger')), default='info')
	date_added = models.DateTimeField(_('Дата добавления'), auto_now_add=True)

	class Meta:
		db_table = 'user_plagin_log'

		verbose_name = _('Журнал плагина пользователя')
		verbose_name_plural = _('Журналы плагинов пользователей')

	def __str__(self) -> str:
		return self.plagin.name
