from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from django.utils.translation import gettext_lazy as _

from ckeditor.widgets import CKEditorWidget

from django.db import models
from updates.models import Update


@admin.register(Update)
class UpdateAdmin(TranslationAdmin):
	list_display = ('title', 'views', 'show_comments_number', 'show_likes_number','date_added')

	fields = ('image', 'title', 'description')
	formfield_overrides = {models.TextField: {'widget': CKEditorWidget}}

	@admin.display(description=_('Количество комментариев'))
	def show_comments_number(self, update: Update) -> int:
		return update.comments.count()

	@admin.display(description=_('Количество лайков'))
	def show_likes_number(self, update: Update) -> int:
		print(update)
		return update.likes.count()
