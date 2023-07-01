from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from django.utils.translation import gettext_lazy as _
from django.utils import html

from ckeditor.widgets import CKEditorWidget

from django.db import models
from instruction.models import InstructionSection


@admin.register(InstructionSection)
class InstructionSectionAdmin(TranslationAdmin):
	ordering = ('position',)

	list_display = ('position', 'show_instruction_section_title', 'last_update')
	list_display_links = None

	fields = ('position', 'title', 'text')
	formfield_overrides = {models.TextField: {'widget': CKEditorWidget}}

	@admin.display(description=_('Заголовок'))
	def show_instruction_section_title(self, instruction_section: InstructionSection) -> str:
		return html.format_html(f'<a href="{instruction_section.id}/change/">{instruction_section.title}<a>')
