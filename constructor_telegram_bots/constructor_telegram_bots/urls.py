from django.urls import re_path, path, include
from django.db.utils import OperationalError
from django.views.static import serve
from django.conf import settings

from telegram_bot.telegram_bots.functions import start_all_telegram_bots

import sys


urlpatterns = [
	re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),

	path('user/', include('user.urls')),
	path('telegram-bot/', include('telegram_bot.urls')),

	path('', include('home.urls')),
	path('donation/', include('donation.urls')),
	path('personal-cabinet/', include('personal_cabinet.urls')),

	path('learn-more/', include('learn_more.urls')),
	path('privacy-policy/', include('privacy_policy.urls')),
]

if settings.DEBUG:
	import debug_toolbar
	
	urlpatterns += [
		path('__debug__/', include(debug_toolbar.urls)),
	]

if sys.argv[1] == 'runserver':
	try:
		start_all_telegram_bots()
	except OperationalError:
		pass
