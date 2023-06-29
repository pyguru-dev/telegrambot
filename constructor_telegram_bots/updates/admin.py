from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from ckeditor.widgets import CKEditorWidget

from django.db import models
from updates.models import Update


@admin.register(Update)
class UpdateAdmin(TranslationAdmin):
	list_display = ('title', '_date_added')

	fields = ('image', 'title', 'description')
	formfield_overrides = {models.TextField: {'widget': CKEditorWidget}}
