from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
	date_hierarchy = 'date_joined'
	list_filter = ('is_staff',)

	list_display = ('id', 'telegram_id', 'first_name', 'show_telegram_bots_count', 'is_staff', 'last_login', 'date_joined')

	fields = ('telegram_id', 'first_name', 'show_telegram_bots_count', 'is_staff', 'groups', 'last_login', 'date_joined')
	readonly_fields = ('telegram_id', 'first_name', 'show_telegram_bots_count', 'last_login', 'date_joined')

	@admin.display(description=_('Количество Telegram ботов'))
	def show_telegram_bots_count(self, user: User) -> int:
		return user.telegram_bots.count()
