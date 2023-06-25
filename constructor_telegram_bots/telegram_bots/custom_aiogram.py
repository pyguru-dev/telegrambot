from aiogram.utils.exceptions import TerminatedByOtherGetUpdates
from aiogram.dispatcher import Dispatcher
from aiohttp.helpers import sentinel
from aiogram import Bot, types

import asyncio
import aiohttp

import logging


log = logging.getLogger('aiogram')


class CustomDispatcher(Dispatcher):
	def __init__(self, bot_username: str, bot: Bot):
		self.bot_username = bot_username

		super().__init__(bot)

	async def start_polling(self, timeout: int = 20, reset_webhook=None):
		log.info('Telegram Bot is started.')

		Dispatcher.set_current(self)
		Bot.set_current(self.bot)

		await self.reset_webhook(
			check=False if reset_webhook is None else True
		)

		self._polling = True
		offset = None

		current_request_timeout = self.bot.timeout

		if current_request_timeout is not sentinel and timeout is not None:
			request_timeout = aiohttp.ClientTimeout(total=current_request_timeout.total + timeout or 1)
		else:
			request_timeout = None

		while self._polling:
			try:
				with self.bot.request_timeout(request_timeout):
					updates: list[types.Update] = await self.bot.get_updates(offset=offset, timeout=timeout)

					try:
						log.info(f'@{self.bot_username} || {updates[-1].message.from_user.first_name}: {updates[-1].message.text}')
					except:
						pass
			except TerminatedByOtherGetUpdates:
				log.error('Telegram Bot already started!')
				break
			except asyncio.CancelledError:
				break
			except Exception as e:
				log.exception('Cause exception while getting updates!')
				break

			if updates:
				offset = updates[-1].update_id + 1

				asyncio.create_task(self._process_polling_updates(updates))

			await asyncio.sleep(0.1)

		self._close_waiter.set_result(None)

		log.info('Telegram Bot is stopped.')
