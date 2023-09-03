from django.db import models
from django.utils.translation import gettext_lazy as _


class Donation(models.Model):
	sum = models.FloatField(_('Сумма'))
	telegram_url = models.CharField(_('Ссылка на Telegram'), max_length=255)
	date = models.DateTimeField(_('Дата'))

	class Meta:
		db_table = 'donation'
		ordering = ['-date']

		verbose_name = _('Пожертвование')
		verbose_name_plural = _('Пожертвования')

	def __str__(self) -> str:
		return self.telegram_url
