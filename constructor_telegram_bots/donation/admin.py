from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html

from .models import Donation


@admin.register(Donation)
class TeamMemberAdmin(admin.ModelAdmin):
	date_hierarchy = 'date'

	list_display = ('id', 'show_sum', 'show_telegram_url', 'date')
	fields = ('sum', 'telegram_url', 'date')

	@admin.display(description=_('Сумма'), ordering='sum')
	def show_sum(self, donation: Donation) -> str:
		return f'{donation.sum}€'

	@admin.display(description=_('Ссылка на Telegram'), ordering='telegram_url')
	def show_telegram_url(self, donation: Donation) -> str:
		return format_html(f'<a href="{donation.telegram_url}" target="_blank">{donation.telegram_url}</a>')
