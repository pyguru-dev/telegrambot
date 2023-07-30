from django.urls import path

from . import views


urlpatterns = [
	path('', views.TelegramBotsView.as_view(), name='telegram_bots'), # POST, GET
    path('<int:telegram_bot_id>/', views.TelegramBotView.as_view(), name='telegram_bot'), # PATCH, DELETE, GET

	path('<int:telegram_bot_id>/start/', views.start_telegram_bot, name='start_telegram_bot'), # POST
	path('<int:telegram_bot_id>/stop/', views.stop_telegram_bot, name='stop_telegram_bot'), # POST

	path('<int:telegram_bot_id>/commands/', views.TelegramBotCommandsView.as_view(), name='telegram_bot_commands'), # POST, GET
	path('<int:telegram_bot_id>/commands/<int:telegram_bot_command_id>/', views.TelegramBotCommandView.as_view(), name='telegram_bot_command'), # PATCH, DELETE, GET

	path('<int:telegram_bot_id>/command/<int:telegram_bot_command_id>/keyboard-button/<int:telegram_bot_command_keyboard_button_id>/add-telegram-bot-command/', views.add_telegram_bot_command_keyboard_button_telegram_bot_command, name='add_telegram_bot_command_keyboard_button_telegram_bot_command'),
	path('<int:telegram_bot_id>/command/<int:telegram_bot_command_id>/keyboard-button/<int:telegram_bot_command_keyboard_button_id>/delete-telegram-bot-command/', views.delete_telegram_bot_command_keyboard_button_telegram_bot_command, name='delete_telegram_bot_command_keyboard_button_telegram_bot_command'),

	path('<int:telegram_bot_id>/user/<int:telegram_bot_user_id>/add-allowed-user/', views.add_allowed_user, name='add_allowed_user'),
	path('<int:telegram_bot_id>/user/<int:telegram_bot_user_id>/delete-allowed-user/', views.delete_allowed_user, name='delete_allowed_user'),
	path('<int:telegram_bot_id>/user/<int:telegram_bot_user_id>/delete/', views.delete_telegram_bot_user, name='delete_telegram_bot_user'),

	path('<int:telegram_bot_id>/save-diagram-current-scale/', views.save_telegram_bot_diagram_current_scale, name='save_telegram_bot_diagram_current_scale'),
	path('<int:telegram_bot_id>/command/<int:telegram_bot_command_id>/save-position/', views.save_telegram_bot_command_position, name='save_telegram_bot_command_position'),

	path('<int:telegram_bot_id>/get-users/', views.get_telegram_bot_users, name='get_telegram_bot_users'),

	path('<int:telegram_bot_id>/database/records/', views.TelegramBotDatabeseRecordsView.as_view(), name='telegram_bot_databese_records'),
    path('<int:telegram_bot_id>/database/records/<int:record_id>/', views.TelegramBotDatabeseRecordView.as_view(), name='telegram_bot_databese_record'),
]
