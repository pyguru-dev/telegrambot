from django.contrib import admin
from konstruktor.models import TelegramBotModel, TelegramBotLogModel, TelegramBotCommandModel

# Register your models here.
@admin.register(TelegramBotModel)
class TelegramBotModelAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'online')