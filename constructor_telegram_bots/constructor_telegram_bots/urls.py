"""constructor_telegram_bots URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
	1. Add an import:  from my_app import views
	2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
	1. Add an import:  from other_app.views import Home
	2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
	1. Import the include() function: from django.urls import include, path
	2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import re_path, path, include
from django.views.static import serve
from django.conf import settings
from django.contrib import admin

from scripts.functions import start_all_telegram_bots

urlpatterns = [
	re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
	re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),

	path('admin/', admin.site.urls),
	path('', include('home.urls')),
	path('user/', include('user.urls')),
	path('telegram_bot/', include('telegram_bot.urls')),
	path('personal_cabinet/', include('personal_cabinet.urls')),
]

start_all_telegram_bots()