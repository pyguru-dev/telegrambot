from django.contrib import admin

from .models import *


@admin.register(Plugin)
class PluginAdmin(admin.ModelAdmin):
	date_hierarchy = 'added_date'
	list_filter = ('is_checked', 'added_date')

	list_display = ('id', 'user', 'telegram_bot', 'name', 'is_checked', 'added_date')
	fields = ('user', 'telegram_bot', 'name', 'code', 'is_checked')

@admin.register(PluginLog)
class PluginLogAdmin(admin.ModelAdmin):
	date_hierarchy = 'added_date'
	list_filter = ('level', 'added_date')

	list_display = ('id', 'user', 'telegram_bot', 'plugin', 'message', 'level', 'added_date')
	fields = ('user', 'telegram_bot', 'plugin', 'message', 'level')
