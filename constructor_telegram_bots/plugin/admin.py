from django.contrib import admin

from .models import Plugin, PluginLog


@admin.register(Plugin)
class PluginAdmin(admin.ModelAdmin):
	date_hierarchy = 'added_date'
	list_filter = ('is_checked',)

	list_display = ('id', 'user', 'telegram_bot', 'name', 'is_checked')
	fields = ('user', 'telegram_bot', 'name', 'code', 'is_checked')

@admin.register(PluginLog)
class PluginLogAdmin(admin.ModelAdmin):
	date_hierarchy = 'added_date'
	list_filter = ('level',)

	list_display = ('id', 'user', 'telegram_bot', 'plugin', 'message', 'level')
	fields = ('user', 'telegram_bot', 'plugin', 'message', 'level')
