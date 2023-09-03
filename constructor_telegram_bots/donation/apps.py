from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DonationConfig(AppConfig):
	default_auto_field = 'django.db.models.BigAutoField'

	name = 'donation'
	verbose_name = _('Пожертвования')
