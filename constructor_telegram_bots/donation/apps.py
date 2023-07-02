from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DonationConfig(AppConfig):
	name = 'donation'
	verbose_name = _('Пожертвования')
