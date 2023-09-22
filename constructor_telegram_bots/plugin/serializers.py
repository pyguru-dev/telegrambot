from django.utils.translation import gettext as _

from rest_framework import serializers

from telegram_bot.models import TelegramBot

import re


class CreatePluginSerializer(serializers.Serializer):
	name = serializers.CharField(max_length=255, error_messages={
		'blank': _('Введите название плагина!'),
		'max_length': _('Название плагина должно содержать не более 255 символов!'),
	})
	code = serializers.CharField()

	def validate_name(self, name: str) -> str:
		telegram_bot: TelegramBot = self.context['telegram_bot']

		if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', name) is None:
			raise serializers.ValidationError(_('Название плагина содержит запрещенные символы!'))

		if telegram_bot.plugins.filter(name=name).exists():
			raise serializers.ValidationError(_('У вас уже добавлен плагин с таким названием!'))

		return name

class UpdatePluginSerializer(serializers.Serializer):
	code = serializers.CharField()

class AddPluginLogSerializer(serializers.Serializer):
	message = serializers.CharField()
	level = serializers.ChoiceField(choices=['info', 'success', 'danger'])
