from django.contrib import admin
from konstruktor.models import TelegramBotModel, TelegramBotLogModel, TelegramBotCommandModel

# Register your models here.
@admin.register(TelegramBotModel)
class TelegramBotModelAdmin(admin.ModelAdmin):
	list_display = ('id', 'owner', 'name', 'online')

@admin.register(TelegramBotLogModel)
class TelegramBotLogModelAdmin(admin.ModelAdmin):
	list_display = ('id', 'owner', 'bot_id')

@admin.register(TelegramBotCommandModel)
class TelegramBotCommandModelAdmin(admin.ModelAdmin):
	list_display = ('id', 'owner', 'bot_id', 'command')