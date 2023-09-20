from django.db import models
from django.utils.translation import gettext_lazy as _


class TeamMember(models.Model):
	image = models.ImageField(upload_to='team/')
	username = models.CharField('@username', max_length=32)
	speciality = models.CharField(_('Специальность'), max_length=255)
	joined_date = models.DateTimeField(_('Присоединился'))

	class Meta:
		db_table = 'team_member'

		verbose_name = _('Члена')
		verbose_name_plural = _('Члены')

	def delete(self) -> None:
		self.image.delete(save=False)
		return super().delete()

	def __str__(self) -> str:
		return f'@{self.username}'
