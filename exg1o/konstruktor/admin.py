from django.contrib import admin
from konstruktor.models import TelegramBotModel, TelegramBotLogModel, TelegramBotCommandModel

# Register your models here.
admin.site.register(TelegramBotModel)
admin.site.register(TelegramBotLogModel)
admin.site.register(TelegramBotCommandModel)