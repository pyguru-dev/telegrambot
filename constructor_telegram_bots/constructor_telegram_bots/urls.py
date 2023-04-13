from django.urls import re_path, path, include
from django.views.static import serve
from django.conf import settings
from django.contrib import admin

import scripts.functions as Functions

urlpatterns = [
	re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
	re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),

	path('admin/', admin.site.urls),
	path('', include('home.urls')),
	path('user/', include('user.urls')),
	path('telegram_bot/', include('telegram_bot.urls')),
	path('personal_cabinet/', include('personal_cabinet.urls')),
]

if Functions.if_find_folder_or_file('./data', 'constructor_telegram_bot.token'):
	Functions.start_all_telegram_bots()
