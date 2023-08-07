from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from ckeditor.widgets import CKEditorWidget

from django.db import models
from .models import Update


@admin.register(Update)
class UpdateAdmin(TranslationAdmin):
	date_hierarchy = 'date_added'

	list_display = ('title', 'date_added')

	fields = ('image', 'title', 'description')
	formfield_overrides = {models.TextField: {'widget': CKEditorWidget}}