from aiogram import types

from telegram_bot.models import (
	TelegramBot,
	TelegramBotCommand,
	TelegramBotCommandKeyboard
)

from asgiref.sync import sync_to_async

from typing import Union
import jinja2


async def search_telegram_bot_command(
	telegram_bot: TelegramBot,
	message_text: str = None,
	button_id: int = None
) -> Union[TelegramBotCommand, None]:
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

async def get_text_variables(message: types.Message, callback_query: Union[types.CallbackQuery, None]) -> dict:
	if not callback_query:
		text_variables = {
			'user_id': message.from_user.id,
			'user_username': message.from_user.username,
			'user_first_name': message.from_user.first_name,
			'user_last_name': message.from_user.last_name,
			'user_message_id': message.message_id,
			'user_message_text': message.text,
		}
	else:
		text_variables = {
			'user_id': callback_query.from_user.id,
			'user_username': callback_query.from_user.username,
			'user_first_name': callback_query.from_user.first_name,
			'user_last_name': callback_query.from_user.last_name,
			'user_message_id': message.message_id,
			'user_message_text': message.text,
		}

	return text_variables

async def replace_text_variables(text: str, text_variables: dict) -> str:
	try:
		jinja2_env = jinja2.Environment(enable_async=True)
		jinja2_template: jinja2.Template = jinja2_env.from_string(text)
		result: str = await jinja2_template.render_async(text_variables)
		return result.replace('\n\n', '\n')
	except Exception as exception:
		return f'{exception.args[0].capitalize()}!'

async def get_telegram_keyboard(command: TelegramBotCommand) -> Union[types.ReplyKeyboardMarkup, types.InlineKeyboardMarkup]:
	telegram_bot_command_keyboard: TelegramBotCommandKeyboard =  await sync_to_async(command.get_keyboard)()

	if telegram_bot_command_keyboard:
		telegram_keyboard_buttons = {}

		for num in range(await telegram_bot_command_keyboard.buttons.acount()):
			telegram_keyboard_buttons.update({num + 1: []})

		telegram_keyboard_row = 1

		if telegram_bot_command_keyboard.type == 'default':
			telegram_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

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
