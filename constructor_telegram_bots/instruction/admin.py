from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from django.utils.translation import gettext_lazy as _

from ckeditor.widgets import CKEditorWidget

from django.db import models
from .models import InstructionSection


@admin.register(InstructionSection)
class InstructionSectionAdmin(TranslationAdmin):
	list_display = ('id', 'position', 'title')

	fields = ('position', 'title', 'text')
	formfield_overrides = {models.TextField: {'widget': CKEditorWidget}}
