from django.urls import path
from konstruktor.views import *

urlpatterns = [
	path('', main_konstruktor_page),
	path('add_bot/', add_bot_page),
	path('add_bot_/', add_bot),
	path('delete_bot/', delete_bot),
	path('view_bot/<str:bot_name>/', view_konstruktor_bot_page),
	path('view_bot/<str:bot_name>/start_bot/', start_bot),
	path('view_bot/<str:bot_name>/add_command/', add_command_page),
	path('view_bot/<str:bot_name>/add_command_/', add_command),
	path('view_bot/<str:bot_name>/view_command/<int:command_id>/', view_command),
	path('view_bot/<str:bot_name>/view_command/<int:command_id>/save_command/', save_command),
	path('view_bot/<str:bot_name>/view_command/<int:command_id>/delete_command/', delete_command)
]
