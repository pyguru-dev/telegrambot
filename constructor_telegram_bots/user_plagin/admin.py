from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from user_plagin.models import UserPlagin, UserPlaginLog


@admin.register(UserPlagin)
class UserPlaginAdmin(admin.ModelAdmin):
	date_hierarchy = 'date_added'
	list_filter = ('is_checked',)

	list_display = ('id', 'user', 'telegram_bot', 'name', 'is_checked')
	fields = ('user', 'telegram_bot', 'name', 'code', 'is_checked')


@admin.register(UserPlaginLog)
class UserPlaginLogAdmin(admin.ModelAdmin):
	date_hierarchy = 'date_added'
	list_filter = ('level',)

	list_display = ('id', 'user', 'telegram_bot', 'plagin', 'message', 'level')
	fields = ('user', 'telegram_bot', 'plagin', 'message', 'level')
