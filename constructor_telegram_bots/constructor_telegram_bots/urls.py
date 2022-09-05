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

from django.db.utils import OperationalError
from django.contrib import admin
from django.urls import path, include
from constructor.models import TelegramBotModel
from telegram_bot import TelegramBot
from threading import Thread

urlpatterns = [
	path('admin/', admin.site.urls),
	path('', include('main.urls')),
	path('', include('authorization.urls')),
	path('', include('registration.urls')),
	path('account/', include('account.urls')),
	path('constructor/<str:username>/', include('constructor.urls'))
]

# Запуск online ботов
try:
	for bot in TelegramBotModel.objects.filter(online=True):
		telegram_bot = TelegramBot(bot.id, bot.token)
		if telegram_bot.auth():
			Thread(target=telegram_bot.start, daemon=True).start()
except OperationalError:
	pass