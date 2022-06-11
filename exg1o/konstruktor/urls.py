from django.urls import path
from konstruktor.views import *

urlpatterns = [
	path('', main_konstruktor_page),
	path('delete_bot/', delete_bot),
	path('add_bot/', add_bot_page),
	path('add_bot_/', add_bot),
	path('view_bot/<int:bot_id>/', view_konstruktor_bot_page),
	path('view_bot/<int:bot_id>/save_bot_settings/', save_bot_settings),
	path('view_bot/<int:bot_id>/start_bot/', start_bot),
	path('view_bot/<int:bot_id>/stop_bot/', stop_bot),
	path('view_bot/<int:bot_id>/add_command/', add_command_page),
	path('view_bot/<int:bot_id>/clear_log/', clear_log),
	path('view_bot/<int:bot_id>/add_command_/', add_command),
	path('view_bot/<int:bot_id>/view_command/<int:command_id>/', view_command),
	path('view_bot/<int:bot_id>/view_command/<int:command_id>/save_command/', save_command),
	path('view_bot/<int:bot_id>/view_command/<int:command_id>/delete_command/', delete_command)
]
