from aiogram import types

from django.db import models

from telegram_bot.models import *
from telegram_bot.services import database_telegram_bot

from asgiref.sync import sync_to_async
from typing import Optional, Union


async def search_telegram_bot_command(
	telegram_bot: TelegramBot,
	message_text: Optional[str] = None,
	button_id: Optional[int] = None
) -> Optional[TelegramBotCommand]:
	if message_text:
		async for telegram_bot_command in telegram_bot.commands.all():
			telegram_bot_command_keyboard: TelegramBotCommandKeyboard = await telegram_bot_command.aget_keyboard()

			if telegram_bot_command_keyboard and telegram_bot_command_keyboard.mode == 'default':
				async for telegram_bot_command_keyboard_button in telegram_bot_command_keyboard.buttons.all():
					if telegram_bot_command_keyboard_button.text == message_text:
						return await telegram_bot_command_keyboard_button.aget_telegram_bot_command()
	elif button_id:
		telegram_bot_command_keyboard_button_: models.Manager = await sync_to_async(TelegramBotCommandKeyboardButton.objects.filter)(id=button_id)

		if await telegram_bot_command_keyboard_button_.aexists():
			telegram_bot_command_keyboard_button: TelegramBotCommandKeyboardButton = await telegram_bot_command_keyboard_button_.afirst()
			return await telegram_bot_command_keyboard_button.aget_telegram_bot_command()

async def get_text_variables(
	telegram_bot: TelegramBot,
	request: Union[types.Message, types.CallbackQuery]
) -> dict:
	database_records = {}

	for record in database_telegram_bot.get_records(telegram_bot):
		database_records[record['_id']] = record

	text_variables = {
		'user_id': request.from_user.id,
		'user_username': request.from_user.username,
		'user_first_name': request.from_user.first_name,
		'user_last_name': request.from_user.last_name,
		'user_message_id': request.message_id if isinstance(request, types.Message) else request.message.message_id,
		'user_message_text': request.text if isinstance(request, types.Message) else request.message.text,
		'database_records': database_records,
	}

	return text_variables

async def get_telegram_keyboard(command: TelegramBotCommand) -> Union[types.ReplyKeyboardMarkup, types.InlineKeyboardMarkup]:
	telegram_bot_command_keyboard: TelegramBotCommandKeyboard =  await sync_to_async(command.get_keyboard)()

	if telegram_bot_command_keyboard:
		telegram_keyboard_buttons = {}

		for num in range(await telegram_bot_command_keyboard.buttons.acount()):
			telegram_keyboard_buttons.update({num + 1: []})

		telegram_keyboard_row = 1

		if telegram_bot_command_keyboard.mode == 'default':
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
