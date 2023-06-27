from django.db import models

from django.utils.translation import gettext_lazy as _


class TeamMembers(models.Model):
	image = models.ImageField(upload_to='static/images/team/')
	username = models.CharField(max_length=32, verbose_name='@username')
	speciality_en = models.CharField(max_length=255, verbose_name=_('Специальность [EN]'))
	speciality_uk = models.CharField(max_length=255, verbose_name=_('Специальность [UK]')) 
	speciality_ru = models.CharField(max_length=255, verbose_name=_('Специальность [RU]')) 
	date_joined = models.DateTimeField(verbose_name=_('Дата присоединения'))

	class Meta:
		db_table = 'team_members'

		verbose_name = _('Члена команды')
		verbose_name_plural = _('Члены команды')
