from django.urls import re_path, path, include
from django.views.static import serve
from django.conf import settings

import scripts.functions as Functions


urlpatterns = [
	re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
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
	
	urlpatterns = [
		path('__debug__/', include(debug_toolbar.urls)),
	] + urlpatterns

if Functions.if_find_folder_or_file(settings.BASE_DIR / 'data', 'constructor_telegram_bot.token'):
	Functions.start_all_telegram_bots()
