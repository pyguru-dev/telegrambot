from django.urls import path, re_path, include
from django.views.static import serve
from django.contrib import admin
from django.conf import settings


urlpatterns = [
	path('user/', include('user.urls')),
	path('telegram-bot/', include('telegram_bot.urls')),

	path('', include('home.urls')),
	path('team/', include('team.urls')),
	path('updates/', include('updates.urls')),
	path('donation/', include('donation.urls')),
	path('personal-cabinet/', include('personal_cabinet.urls')),
	path('privacy-policy/', include('privacy_policy.urls')),

	path("i18n/", include("django.conf.urls.i18n")),
	path('admin/', admin.site.urls),
]


if settings.DEBUG:
	urlpatterns + [re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT})]
