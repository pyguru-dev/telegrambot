from django.urls import re_path, path, include
from django.views.static import serve
from django.conf import settings

from telegram_bots import start_all_telegram_bots

import sys


urlpatterns = [
	re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),

	path('user/', include('user.urls')),
	path('telegram-bot/', include('telegram_bot.urls')),

	path('', include('home.urls')),
	path('donation/', include('donation.urls')),
	path('personal-cabinet/', include('personal_cabinet.urls')),

	path('privacy-policy/', include('privacy_policy.urls')),
]


if sys.argv[1] not in ['test', 'makemigrations', 'migrate']:
	start_all_telegram_bots()
