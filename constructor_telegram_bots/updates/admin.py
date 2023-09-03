from django.contrib import admin
from django.db import models

from modeltranslation.admin import TranslationAdmin
from ckeditor.widgets import CKEditorWidget

from .models import Update


@admin.register(Update)
class UpdateAdmin(TranslationAdmin):
	date_hierarchy = 'added_date'

	list_display = ('version', 'added_date')

	fields = ('image', 'version', 'description')
	formfield_overrides = {models.TextField: {'widget': CKEditorWidget}}
