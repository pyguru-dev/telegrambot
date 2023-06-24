from django.contrib import admin

from django.core.handlers.wsgi import WSGIRequest

from django.contrib.auth.models import Group
from user.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
	date_hierarchy = 'date_joined'

	list_display = (
		'id',
		'username',
		'is_staff',
		'is_superuser',
		'show_telegram_bots_count',
		'last_login',
		'date_joined',
	)
	list_display_links = None

	fields = ('username', 'password', 'is_staff', 'is_superuser')

	@admin.display(description='Количество Telegram ботов')
	def show_telegram_bots_count(self, user: User):
		return user.telegram_bots.count()
	
	def has_change_permission(self, request: WSGIRequest, obj: None=None):
		return False


admin.site.unregister(Group)