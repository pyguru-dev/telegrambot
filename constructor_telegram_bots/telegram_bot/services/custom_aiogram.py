from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiohttp.helpers import sentinel
from aiogram.utils.exceptions import (
	TerminatedByOtherGetUpdates,
	TelegramAPIError,
	ConflictError,
	NetworkError
)

from django.conf import settings

import asyncio
import aiohttp

import logging


log = logging.getLogger('aiogram')


class CustomBot(Bot):
	def __init__(self, *args, **kwargs):
		if not settings.TEST:
			super().__init__(*args, **kwargs)
		else:
			self.results = []

	async def delete_message(self, *args, **kwargs):
		if not settings.TEST:
			return await super().delete_message(*args, **kwargs)
		else:
			self.results.append({'method': 'delete_message'})

	async def send_message(self, *args, **kwargs):
		if not settings.TEST:
			return await super().send_message(*args, **kwargs)
		else:
			kwargs.update({'method': 'send_message'})
			self.results.append(kwargs)

	async def send_photo(self, *args, **kwargs):
		if not settings.TEST:
			return await super().send_photo(*args, **kwargs)
		else:
			kwargs.update({'method': 'send_photo'})
			self.results.append(kwargs)

	async def get_results(self):
		return self.results


class CustomDispatcher(Dispatcher):
	def __init__(self, bot_username: str, bot: CustomBot):
		self.bot_username = bot_username

		super().__init__(bot)

	async def start_polling(self, timeout: int = 20, reset_webhook=None):
		log.info(f'@{self.bot_username} || Telegram bot is starting.')

		Dispatcher.set_current(self)
		Bot.set_current(self.bot)

		await self.reset_webhook(check=False if reset_webhook is None else True)

		self._polling = True
		current_request_timeout = self.bot.timeout
		offset = None

		if current_request_timeout is not sentinel and timeout is not None:
			request_timeout = aiohttp.ClientTimeout(total=current_request_timeout.total + timeout or 1)
		else:
			request_timeout = None

		while self._polling:
			try:
				with self.bot.request_timeout(request_timeout):
					updates: list[types.Update] = await self.bot.get_updates(offset=offset, timeout=timeout)

					for update in updates:
						try:
							log.info(f'@{self.bot_username} || {update.message.from_user.first_name}: {update.message.text}')
						except:
							pass
			except TerminatedByOtherGetUpdates:
				log.error(f'@{self.bot_username} || Telegram bot is already started!')
				break
			except (TelegramAPIError, ConflictError, NetworkError):
				pass
			except asyncio.CancelledError:
				break
			except Exception as e:
				log.exception(f'@{self.bot_username} || Cause exception while getting updates!')
				break

			if updates:
				offset = updates[-1].update_id + 1

				asyncio.create_task(self._process_polling_updates(updates))

			await asyncio.sleep(0.1)

		self._close_waiter.set_result(None)

		log.info(f'@{self.bot_username} || Telegram bot is stopped.')
