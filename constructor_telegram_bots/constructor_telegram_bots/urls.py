from django.urls import path, include
from django.contrib import admin
from django.conf import settings

from telegram_bot.services import tasks

from sys import platform


urlpatterns = [
	path('admin/', admin.site.urls),
	path('i18n/', include('django.conf.urls.i18n')),

	path('user/', include('user.urls')),
	path('', include('home.urls')),
	path('team/', include('team.urls')),
	path('updates/', include('updates.urls')),
	path('instruction/', include('instruction.urls')),
	path('donation/', include('donation.urls')),
	path('personal-cabinet/', include('personal_cabinet.urls')),
	path('telegram-bots/', include('telegram_bot.urls')),
	path('plugins/', include('plugin.urls')),
	path('privacy-policy/', include('privacy_policy.urls')),
]


if settings.DEBUG:
	from django.conf.urls.static import static

	urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if not settings.TEST and platform == 'win32':
	tasks.start_all_telegram_bots()
