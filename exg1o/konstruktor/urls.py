from django.urls import path
from konstruktor.views import *

urlpatterns = [
	path('konstruktor/<str:nickname>/', konstruktor_page),
	path('konstruktor/<str:nickname>/add_bot/', add_bot_page),
	path('konstruktor/<str:nickname>/add_bot_/', add_bot),
]
