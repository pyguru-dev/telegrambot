from django.urls import re_path, path, include
from django.views.static import serve
from django.conf import settings

from telegram_bots import start_all_telegram_bots

import sys


urlpatterns = [
	path('user/', include('user.urls')),
	path('telegram-bot/', include('telegram_bot.urls')),

	path('', include('home.urls')),
	path('donation/', include('donation.urls')),
	path('personal-cabinet/', include('personal_cabinet.urls')),

	path('privacy-policy/', include('privacy_policy.urls')),
]


if settings.DEBUG:
	urlpatterns.append(
		re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT})
	)


if sys.argv[0] == 'manage.py':
	if sys.argv[1] == 'runserver':
		start_all_telegram_bots()
