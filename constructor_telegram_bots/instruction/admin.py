from django.contrib import admin

from modeltranslation.admin import TranslationAdmin
from tinymce.widgets import TinyMCE

from django.db import models

from .models import InstructionSection


@admin.register(InstructionSection)
class InstructionSectionAdmin(TranslationAdmin):
	list_display = ('title', 'position')

	fields = ('title', 'text', 'position')
	formfield_overrides = {
		models.TextField: {
			'widget': TinyMCE,
		},
	}
