from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UserConfig(AppConfig):
	default_auto_field = 'django.db.models.BigAutoField'

	name = 'user'
	verbose_name = _('Пользователи')
