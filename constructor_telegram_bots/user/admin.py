from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from user.models import User, UserPlugin, UserPluginLog


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
	date_hierarchy = 'date_joined'
	list_filter = ('is_staff',)

	list_display = ('id', 'telegram_id', 'username', 'show_telegram_bots_count', 'is_staff', 'last_login', 'date_joined')

	fields = ('telegram_id', 'username', 'show_telegram_bots_count', 'is_staff', 'groups', 'last_login', 'date_joined')
	readonly_fields = ('telegram_id', 'username', 'show_telegram_bots_count', 'last_login', 'date_joined')

	@admin.display(description=_('Количество Telegram ботов'))
	def show_telegram_bots_count(self, user: User) -> int:
		return user.telegram_bots.count()

@admin.register(UserPlugin)
class UserPluginAdmin(admin.ModelAdmin):
	date_hierarchy = 'date_added'
	list_filter = ('is_checked',)

	list_display = ('id', 'user', 'telegram_bot', 'name', 'is_checked')
	fields = ('user', 'telegram_bot', 'name', 'code', 'is_checked')

@admin.register(UserPluginLog)
class UserPluginLogAdmin(admin.ModelAdmin):
	date_hierarchy = 'date_added'
	list_filter = ('level',)

	list_display = ('id', 'user', 'telegram_bot', 'plugin', 'message', 'level')
	fields = ('user', 'telegram_bot', 'plugin', 'message', 'level')
