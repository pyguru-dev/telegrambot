from django.db import models
from django.utils.translation import gettext_lazy as _


class TeamMember(models.Model):
	image = models.ImageField(upload_to='static/images/team/')
	username = models.CharField('@username', max_length=32)
	speciality = models.CharField(_('Специальность'), max_length=255)
	date_joined = models.DateTimeField(_('Дата присоединения'))

	class Meta:
		db_table = 'team_member'

		verbose_name = _('Члена команды')
		verbose_name_plural = _('Члены команды')
