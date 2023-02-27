from django.urls import path
from personal_cabinet.views import *

urlpatterns = [
	path('', personal_cabinet),
    path('<int:telegram_bot_id>/', telegram_bot_menu),
]