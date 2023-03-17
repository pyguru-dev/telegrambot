from django.urls import path
from telegram_bot.views import *

urlpatterns = [
	path('add/', add_telegram_bot),
	path('<int:telegram_bot_id>/duplicate/', duplicate_telegram_bot),
	path('<int:telegram_bot_id>/delete/', delete_telegram_bot),

	path('<int:telegram_bot_id>/start/', start_telegram_bot),
	path('<int:telegram_bot_id>/stop/', stop_telegram_bot),

	path('<int:telegram_bot_id>/edit/private/', edit_telegram_bot_private),

	path('<int:telegram_bot_id>/command/add/', add_telegram_bot_command),
	path('<int:telegram_bot_id>/command/<int:telegram_bot_command_id>/edit/', edit_telegram_bot_command), # !
	path('<int:telegram_bot_id>/command/<int:telegram_bot_command_id>/delete/', delete_telegram_bot_command), # !
	
	path('<int:telegram_bot_id>/user/<int:telegram_bot_user_id>/give_access./', give_telegram_bot_user_access), # !
	path('<int:telegram_bot_id>/user/<int:telegram_bot_user_id>/delete/', delete_telegram_bot_user), # !
	
	path('<int:telegram_bot_id>/get_commands/', get_telegram_bot_commands),
    path('<int:telegram_bot_id>/get_users/', get_telegram_bot_users),
]