from django.urls import path
from constructor.views import *

urlpatterns = [
	path('', main_constructor_page),
	path('delete_bot/', delete_bot),
	path('add_bot/', add_bot_page),
	path('add_bot_/', add_bot),
	path('view_bot/<int:bot_id>/', view_bot_page),
	path('view_bot/<int:bot_id>/save_bot_settings/', save_bot_settings),
	path('view_bot/<int:bot_id>/start_bot/', start_bot),
	path('view_bot/<int:bot_id>/stop_bot/', stop_bot),
	path('view_bot/<int:bot_id>/clear_bot_logs/', clear_bot_logs),
	path('view_bot/<int:bot_id>/get_bot_logs/', get_bot_logs),
	path('view_bot/<int:bot_id>/add_bot_command/', add_bot_command_page),
	path('view_bot/<int:bot_id>/add_bot_command_/', add_bot_command),
	path('view_bot/<int:bot_id>/view_bot_command/<int:command_id>/', view_bot_command_page),
	path('view_bot/<int:bot_id>/view_bot_command/<int:command_id>/save_bot_command/', save_bot_command),
	path('view_bot/<int:bot_id>/<int:command_id>/delete_bot_command/', delete_bot_command)
]
