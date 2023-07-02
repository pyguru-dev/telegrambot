from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils import html

from user.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
	date_hierarchy = 'date_joined'
	list_filter = ('is_staff',)

	list_display = (
		'id',
		'show_username',
		'is_staff',
		'show_telegram_bots_count',
		'last_login',
		'date_joined',
	)
	list_display_links = None

	fields = ('id', 'username', 'is_staff', 'groups')
	readonly_fields = ('id', 'username')

	@admin.display(description=_('Имя пользователя'))
	def show_username(self, user: User) -> str:
		if user.is_staff:
			return html.format_html(f'<a href="{user.id}/change/">{user.username}<a>')
		else:
			return user.username

	@admin.display(description=_('Количество Telegram ботов'))
	def show_telegram_bots_count(self, user: User) -> int:
		return user.telegram_bots.count()
