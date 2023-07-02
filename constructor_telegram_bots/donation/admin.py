from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html

from donation.models import Donation


@admin.register(Donation)
class TeamMemberAdmin(admin.ModelAdmin):
	date_hierarchy = 'date'

	list_display = ('date', 'show_telegram_url', 'show_sum')

	fields = ('date', 'telegram_url', 'sum')

	@admin.action(description=_('Ссылка на Telegram'))
	def show_telegram_url(self, donation: Donation) -> str:
		return format_html(f'<a href="{donation.telegram_url}" target="_blank">{donation.telegram_url}</a>')

	@admin.action(description=_('Сумма'))
	def show_sum(self, donation: Donation) -> str:
		return f'{donation.sum}€'
