from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class InstructionConfig(AppConfig):
	default_auto_field = 'django.db.models.BigAutoField'

	name = 'instruction'
	verbose_name = _('Инструкция')
