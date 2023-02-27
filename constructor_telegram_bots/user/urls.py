from django.urls import path
from user.views import *

urlpatterns = [
	path('auth/<int:user_id>/<str:confirm_code>/', auth),
    path('get_added_telegram_bots/', get_added_telegram_bots),
]