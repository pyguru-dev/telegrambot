from django.db import models

from django.utils.translation import gettext_lazy as _

from django.conf import settings
import pytz


class Updates(models.Model):
	image = models.ImageField(upload_to='static/images/updates/')
	title = models.CharField(_('Заголовок'), max_length=255)
	description = models.TextField(_('Описание'))
	_date_added = models.DateTimeField(_('Дата добавления'), auto_now_add=True)

	class Meta:
		db_table = 'updates'

		verbose_name = _('Обновление')
		verbose_name_plural = _('Обновления')

	@property
	def date_added(self) -> str:
		return self._date_added.astimezone(
			pytz.timezone(settings.TIME_ZONE)
		).strftime('%d.%m.%Y - %H:%M:%S')
