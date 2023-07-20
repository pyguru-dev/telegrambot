from django.db import models
from django.utils.translation import gettext_lazy as _


class InstructionSection(models.Model):
	position = models.IntegerField(_('Позиция'))
	title = models.CharField(_('Заголовок'), max_length=255)
	text = models.TextField(_('Текст'))
	last_update = models.DateTimeField(_('Дата обновления'), auto_now=True)

	class Meta:
		db_table = 'instruction_section'

		ordering = ['position']

		verbose_name = _('Раздел инструкции')
		verbose_name_plural = _('Разделы инструкции')

	def __str__(self) -> str:
		return self.title
