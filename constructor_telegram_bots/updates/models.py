from django.db import models
from django.utils.translation import gettext_lazy as _


class Update(models.Model):
	image = models.ImageField(upload_to='static/images/updates/')
	version = models.CharField(_('Версия'), max_length=255)
	description = models.TextField(_('Описание'))
	added_date = models.DateTimeField(_('Добавлено'), auto_now_add=True)

	class Meta:
		db_table = 'update'
		ordering = ['-added_date']

		verbose_name = _('Обновление')
		verbose_name_plural = _('Обновления')

	def __str__(self) -> str:
		return self.version
