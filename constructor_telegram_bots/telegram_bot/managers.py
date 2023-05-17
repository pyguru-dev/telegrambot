from django.db.models import Manager

import telegram_bot.models as TelegramBotModels
import user.models as UserModels

from telegram_bot.functions import check_telegram_bot_api_token


class TelegramBotManager(Manager):
	def add_telegram_bot(self, user: 'UserModels.User', api_token: str, is_private: bool, **extra_fields) -> 'TelegramBotModels.TelegramBot':
		name: str = check_telegram_bot_api_token(api_token=api_token)

		telegram_bot: TelegramBotModels.TelegramBot = self.model(name=name, api_token=api_token, is_private=is_private, **extra_fields)
		telegram_bot.save()

		user.telegram_bots.add(telegram_bot)
		user.save()

		return telegram_bot


class TelegramBotCommandManager(Manager):
	def add_telegram_bot_command(
		self,
		telegram_bot: 'TelegramBotModels.TelegramBot',
		name: str,
		command: str,
		callback: str,
		message_text: str,
		keyboard: str,
		**extra_fields
	) -> 'TelegramBotModels.TelegramBotCommand':
		telegram_bot_command: TelegramBotModels.TelegramBotCommand = self.model(
			name=name,
			command=command,
			callback=callback,
			message_text=message_text,
			keyboard=keyboard,
			**extra_fields
		)
		telegram_bot_command.save()

		telegram_bot.commands.add(telegram_bot_command)
		telegram_bot.save()

		return telegram_bot_command


class TelegramBotUserManager(Manager):
	def add_telegram_bot_user(self, telegram_bot: 'TelegramBotModels.TelegramBot', user_id: int, username: str) -> 'TelegramBotModels.TelegramBotUser':
		telegram_bot_user: TelegramBotModels.TelegramBotUser = self.model(user_id=user_id, username=username)
		telegram_bot_user.save()

		telegram_bot.users.add(telegram_bot_user)
		telegram_bot.save()

		return telegram_bot_user
