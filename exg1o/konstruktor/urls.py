from django.urls import path
from konstruktor.views import *

urlpatterns = [
	path('', main_konstruktor_page),
	path('add_bot/', add_bot_page),
	path('add_bot_/', add_bot),
	path('delete_bot/', delete_bot),
	path('view_bot/<str:bot_name>/', view_konstruktor_bot_page),
	path('view_bot/<str:bot_name>/add_command/', add_command_page),
	path('view_bot/<str:bot_name>/add_command_/', add_command)
]
