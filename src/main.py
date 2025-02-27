import config
import core

import aiogram
import asyncio
import os

# 
# @self.dispatcher.message(aiogram.F.voice)


class Bot():

	def __init__(self, openai_api_token: str, telegram_token: str):

		#self.engine = core.services.Engine(openai_api_token)
		self.bot = aiogram.Bot(token = telegram_token)
		self.dispatcher = aiogram.Dispatcher()
		self.setup()

	def setup(self):

		@self.dispatcher.message(aiogram.F.text)
		async def handle_text_message(message: aiogram.types.Message):

			await core.handlers.handle_text_message(message)

	async def run(self):

		await self.dispatcher.start_polling(self.bot)

"""




if __name__ == '__main__':




"""


if __name__ == '__main__':

	async def main():

		settings = config.Settings()
		bot = Bot(settings.OPENAI_API_TOKEN.get_secret_value(), settings.TELEGRAM_TOKEN.get_secret_value())
		await bot.run()

	asyncio.run(main())