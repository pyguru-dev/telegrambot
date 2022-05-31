from django.urls import path
from konstruktor.views import *

urlpatterns = [
	path('konstruktor/<str:nickname>/', main_konstruktor_page),
	path('konstruktor/<str:nickname>/view_bot/<str:bot_name>/', view_konstruktor_bot_page),
	path('konstruktor/<str:nickname>/add_bot/', add_bot_page),
	path('konstruktor/<str:nickname>/add_bot_/', add_bot),
	path('konstruktor/<str:nickname>/delete_bot/', delete_bot)
]
