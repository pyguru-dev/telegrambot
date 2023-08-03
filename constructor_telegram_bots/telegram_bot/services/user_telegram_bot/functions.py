from aiogram import types

from telegram_bot.models import TelegramBot, TelegramBotCommand, TelegramBotCommandKeyboard

from telegram_bot.services import database_telegram_bot

from asgiref.sync import sync_to_async
from typing import Optional, Union


async def search_telegram_bot_command(telegram_bot: TelegramBot, message_text: str = None, button_id: int = None) -> Optional[TelegramBotCommand]:
	async for telegram_bot_command in telegram_bot.commands.all():
		telegram_bot_command_keyboard: TelegramBotCommandKeyboard = await sync_to_async(telegram_bot_command.get_keyboard)()

		if telegram_bot_command_keyboard:
			if (
				telegram_bot_command_keyboard.type == 'default' and message_text or
				telegram_bot_command_keyboard.type == 'inline' and button_id
			):
				async for telegram_bot_command_keyboard_button in telegram_bot_command_keyboard.buttons.all():
					if (
						telegram_bot_command_keyboard_button.text == message_text and message_text or
						telegram_bot_command_keyboard_button.id == button_id and button_id
					):
						return await sync_to_async(telegram_bot_command_keyboard_button.get_command)()

async def get_text_variables(telegram_bot: TelegramBot, message: types.Message, callback_query: Optional[types.CallbackQuery]) -> dict:
	if not callback_query:
		text_variables = {
			'user_id': message.from_user.id,
			'user_username': message.from_user.username,
			'user_first_name': message.from_user.first_name,
			'user_last_name': message.from_user.last_name,
		}
	else:
		text_variables = {
			'user_id': callback_query.from_user.id,
			'user_username': callback_query.from_user.username,
			'user_first_name': callback_query.from_user.first_name,
			'user_last_name': callback_query.from_user.last_name,
		}

	database_records = {}

	for record in database_telegram_bot.get_records(telegram_bot):
		database_records[record['_id']] = record

	text_variables.update({
		'user_message_id': message.message_id,
		'user_message_text': message.text,
		'database_records': database_records,
	})

	return text_variables

async def get_telegram_keyboard(command: TelegramBotCommand) -> Union[types.ReplyKeyboardMarkup, types.InlineKeyboardMarkup]:
	telegram_bot_command_keyboard: TelegramBotCommandKeyboard =  await sync_to_async(command.get_keyboard)()

	if telegram_bot_command_keyboard:
		telegram_keyboard_buttons = {}

		for num in range(await telegram_bot_command_keyboard.buttons.acount()):
			telegram_keyboard_buttons.update({num + 1: []})

		telegram_keyboard_row = 1

		if telegram_bot_command_keyboard.type == 'default':
			telegram_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

			async for button in telegram_bot_command_keyboard.buttons.all():
				telegram_keyboard_buttons[telegram_keyboard_row if not button.row else button.row].append(
					types.KeyboardButton(text=button.text)
				)

				telegram_keyboard_row += 1
		else:
			telegram_keyboard = types.InlineKeyboardMarkup()

			async for button in telegram_bot_command_keyboard.buttons.all():
				telegram_keyboard_buttons[telegram_keyboard_row if not button.row else button.row].append(
					types.InlineKeyboardButton(
						text=button.text,
						url=button.url,
						callback_data=button.id
					)
				)

				telegram_keyboard_row += 1

		for telegram_keyboard_button in telegram_keyboard_buttons:
			telegram_keyboard.add(*telegram_keyboard_buttons[telegram_keyboard_button])
	else:
		telegram_keyboard = None

	return telegram_keyboard
