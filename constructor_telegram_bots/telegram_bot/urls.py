from django.urls import path

from . import views


urlpatterns = [
	path('', views.TelegramBotsView.as_view(), name='telegram_bots'), # POST, GET
    path('<int:telegram_bot_id>/', views.TelegramBotView.as_view(), name='telegram_bot'), # PATCH, DELETE, GET
	path('<int:telegram_bot_id>/start_or_stop/', views.start_or_stop_telegram_bot, name='start_or_stop_telegram_bot'), # POST
    path('<int:telegram_bot_id>/update-diagram-current-scale/', views.update_telegram_bot_diagram_current_scale, name='update_telegram_bot_diagram_current_scale'), # PATCH

	path('<int:telegram_bot_id>/commands/', views.TelegramBotCommandsView.as_view(), name='telegram_bot_commands'), # POST, GET
	path('<int:telegram_bot_id>/commands/<int:telegram_bot_command_id>/', views.TelegramBotCommandView.as_view(), name='telegram_bot_command'), # PATCH, DELETE, GET
	path('<int:telegram_bot_id>/commands/<int:telegram_bot_command_id>/update-position/', views.update_telegram_bot_command_position, name='update_telegram_bot_command_position'), # PATCH
	path('<int:telegram_bot_id>/commands/<int:telegram_bot_command_id>/keyboard-buttons/<int:telegram_bot_command_keyboard_button_id>/telegram-bot-command/', views.TelegramBotCommandKeyboardButtonTelegramBotCommandView.as_view(), name='telegram_bot_command_keyboard_button_telegram_bot_command'), # POST, DELETE

	path('<int:telegram_bot_id>/users/', views.TelegramBotUsersView.as_view(), name='telegram_bot_users'), # GET
	path('<int:telegram_bot_id>/users/<int:telegram_bot_user_id>/', views.TelegramBotUserView.as_view(), name='telegram_bot_user'), # DELETE
	path('<int:telegram_bot_id>/users/<int:telegram_bot_user_id>/allowed-user/', views.TelegramBotAllowedUserView.as_view(), name='telegram_bot_allowed_user'), # POST, DELETE

	path('<int:telegram_bot_id>/database/records/', views.TelegramBotDatabeseRecordsView.as_view(), name='telegram_bot_databese_records'), # POST, GET
    path('<int:telegram_bot_id>/database/records/<int:record_id>/', views.TelegramBotDatabeseRecordView.as_view(), name='telegram_bot_databese_record'), # PATCH, DELETE
]
