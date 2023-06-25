from django.contrib import admin

from django.core.handlers.wsgi import WSGIRequest
from django.utils import html

from user.models import User

from typing import Union


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

	fields = ('username', 'password', 'is_staff', 'groups')

	@admin.display(description='Имя пользователя')
	def show_username(self, user: User):
		if user.is_staff:
			return html.format_html(f'<a href="{user.id}/change/">{user.username}<a>')
		else:
			return user.username

	@admin.display(description='Количество Telegram ботов')
	def show_telegram_bots_count(self, user: User):
		return user.telegram_bots.count()
	
	def has_change_permission(self, request: WSGIRequest, user: Union[User, None]=None):
		if user is not None:
			if user.is_staff:
				return True
		return False
