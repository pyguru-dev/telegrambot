from django.db import models
from django.utils.translation import gettext_lazy as _


class Update(models.Model):
	image = models.ImageField(upload_to='static/images/updates/')
	title = models.CharField(_('Заголовок'), max_length=255)
	description = models.TextField(_('Описание'))
	date_added = models.DateTimeField(_('Дата добавления'), auto_now_add=True)

	class Meta:
		db_table = 'update'

		verbose_name = _('Обновление')
		verbose_name_plural = _('Обновления')

	def __str__(self) -> str:
		return self.title
