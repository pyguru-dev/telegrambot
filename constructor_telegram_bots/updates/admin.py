from django.contrib.admin import register
from modeltranslation.admin import TranslationAdmin

from ckeditor.widgets import CKEditorWidget

from django.db import models
from updates.models import Updates


@register(Updates)
class UpdatesAdmin(TranslationAdmin):
	list_display = ('title', '_date_added')

	fields = ('image', 'title', 'description')
	formfield_overrides = {models.TextField: {'widget': CKEditorWidget}}
