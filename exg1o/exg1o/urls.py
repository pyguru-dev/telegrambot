"""exg1o URL Configuration

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

from django.contrib import admin
from django.urls import path, include
from konstruktor.models import TelegramBotModel
from telegram_bot import TelegramBot
import global_variable as GlobalVariable
from threading import Thread

urlpatterns = [
	path('admin/', admin.site.urls),
	path('', include('main.urls')),
	path('', include('authorization.urls')),
	path('', include('registration.urls')),
	path('account/', include('account.urls')),
	path('account/konstruktor/<str:nickname>/', include('konstruktor.urls'))
]

for bot in TelegramBotModel.objects.filter(online=True):
	telegram_bot = TelegramBot(bot.owner, bot.id, bot.token)
	if telegram_bot.auth():
		Thread(target=telegram_bot.start, daemon=True).start()

		GlobalVariable.online_bots.update(
			{
				bot.owner: {
					bot.id: telegram_bot
				}
			}
		)