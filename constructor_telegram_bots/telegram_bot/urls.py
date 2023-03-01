from django.urls import path
from telegram_bot.views import *

urlpatterns = [
	path('add/', add),
	path('<int:telegram_bot_id>/delete/', delete),

	path('<int:telegram_bot_id>/start/', start),
	path('<int:telegram_bot_id>/stop/', stop),

	path('<int:telegram_bot_id>/edit/private/', edit_private),
]