from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from user.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
	date_hierarchy = 'date_joined'
	list_filter = ('is_staff',)

	list_display = (
		'id',
		'username',
		'is_staff',
		'show_telegram_bots_count',
		'last_login',
		'date_joined',
	)
	fields = ('username', 'is_staff', 'groups')

	@admin.display(description=_('Количество Telegram ботов'))
	def show_telegram_bots_count(self, user: User) -> int:
		return user.telegram_bots.count()
