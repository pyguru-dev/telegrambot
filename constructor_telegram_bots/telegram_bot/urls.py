from django.urls import path
from telegram_bot.views import *

urlpatterns = [
	path('add/', add),
]