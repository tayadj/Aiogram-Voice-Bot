import config
import core
import data

import aiogram
import asyncio
import os



class Bot():

	def __init__(self, settings):

		self.engine = core.services.Engine(settings.OPENAI_API_TOKEN.get_secret_value(), settings.OPENAI_API_ASSISTANT.get_secret_value())
		self.database = data.Database(settings.DATABASE_URL.get_secret_value())

		self.bot = aiogram.Bot(token = settings.TELEGRAM_TOKEN.get_secret_value())
		self.dispatcher = aiogram.Dispatcher()

		self.commands_setup()
		self.handlers_setup()

	def commands_setup(self):

		async def run():

			commands = [
				aiogram.types.BotCommand(command = '/profile', description = 'Show profile')
			]
			await self.bot.set_my_commands(commands = commands)

		asyncio.create_task(run())

	def handlers_setup(self):

		@self.dispatcher.message(aiogram.filters.Command('start'))
		async def handle_profile_command(message: aiogram.types.Message):

			await core.handlers.handle_start_command(message, self.engine, self.database)

		@self.dispatcher.message(aiogram.filters.Command('profile'))
		async def handle_profile_command(message: aiogram.types.Message):

			await core.handlers.handle_profile_command(message, self.engine, self.database)

		@self.dispatcher.message(aiogram.F.text)
		async def handle_text_message(message: aiogram.types.Message):

			await core.handlers.handle_text_message(message, self.database)

		@self.dispatcher.message(aiogram.F.voice)
		async def handle_voice_message(message: aiogram.types.Message):

			await core.handlers.handle_voice_message(message, self.engine, self.database)

	async def run(self):

		await self.dispatcher.start_polling(self.bot)



if __name__ == '__main__':

	async def main():

		settings = config.Settings()
		bot = Bot(settings)
		await bot.run()

	asyncio.run(main())