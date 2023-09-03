from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
	search_fields = ('first_name',)
	date_hierarchy = 'date_joined'
	list_filter = ('is_staff', 'date_joined')

	list_display = ('id', 'telegram_id', 'first_name', 'telegram_bots_count', 'is_staff', 'last_login', 'date_joined')

	fields = ('id', 'telegram_id', 'first_name', 'telegram_bots_count', 'is_staff', 'groups', 'last_login', 'date_joined')
	readonly_fields = ('id', 'telegram_id', 'first_name', 'telegram_bots_count', 'last_login', 'date_joined')

	@admin.display(description=_('Количество Telegram ботов'))
	def telegram_bots_count(self, user: User) -> int:
		return user.telegram_bots.count()

	def has_add_permission(self, *args, **kwargs) -> bool:
		return False
