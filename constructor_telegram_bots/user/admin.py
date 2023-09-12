from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
	search_fields = ('first_name',)
	date_hierarchy = 'joined_date'
	list_filter = ('is_staff', 'joined_date')

	list_display = ('id', 'telegram_id', 'first_name', 'telegram_bots_count', 'is_staff', 'last_login', 'joined_date')

	fields = ('id', 'telegram_id', 'first_name', 'telegram_bots_count', 'is_staff', 'groups', 'last_login', 'joined_date')
	readonly_fields = ('id', 'telegram_id', 'first_name', 'telegram_bots_count', 'last_login', 'joined_date')

	@admin.display(description=_('Количество Telegram ботов'))
	def telegram_bots_count(self, user: User) -> int:
		return user.telegram_bots.count()

	def has_add_permission(self, *args, **kwargs) -> bool:
		return False
