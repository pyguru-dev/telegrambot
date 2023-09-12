from django.contrib import admin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import html

from modeltranslation.admin import TranslationAdmin
from ckeditor.widgets import CKEditorWidget

from .models import *


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
	date_hierarchy = 'date'

	list_display = ('id', 'sum_', 'telegram_url_', 'date')
	fields = ('sum', 'telegram_url', 'date')

	@admin.display(description=_('Сумма'), ordering='sum')
	def sum_(self, donation: Donation) -> str:
		return f'{donation.sum}€'

	@admin.display(description=_('Telegram'), ordering='telegram_url')
	def telegram_url_(self, donation: Donation) -> str:
		return html.format_html(f'<a href="{donation.telegram_url}" style="font-weight: 600;" target="_blank">{donation.telegram_url}</a>')

@admin.register(DonationSection)
class DonationSectionAdmin(TranslationAdmin):
	list_display = ('title', 'position')

	fields = ('title', 'text', 'position')
	formfield_overrides = {models.TextField: {'widget': CKEditorWidget}}
