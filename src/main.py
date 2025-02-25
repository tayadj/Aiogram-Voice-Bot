import aiogram
import asyncio
import openai
import os
import pydantic
import pydantic_settings



class Settings(pydantic_settings.BaseSettings):
	
	model_config = pydantic_settings.SettingsConfigDict(
		env_file = '.env', env_file_encoding = 'utf-8', extra = 'ignore'
	)

	OPENAI_API_TOKEN: pydantic.SecretStr
	TELEGRAM_TOKEN: pydantic.SecretStr

settings = Settings()



class Engine():

	def __init__(self, openai_api_token: str):

		self.client = openai.AsyncOpenAI(api_key = openai_api_token)

		self.assistant = None
		self.thread = None

		self.setup_event = asyncio.Event()
		asyncio.create_task(self.assistant_setup())

	async def assistant_setup(self):

		self.assistant = await self.client.beta.assistants.create(
			model = 'gpt-3.5-turbo',
			instructions = 'You are a search assistant.'
		)
		self.thread = await self.client.beta.threads.create()

		self.setup_event.set()

	async def voice_to_text(self, path: str) -> str:

		with open(path, 'rb') as voice_file:

			response = await self.client.audio.transcriptions.create(
				file = voice_file, 
				model = 'whisper-1'
			)

		return response.text

	async def text_to_voice(self, text: str, path: str):

		response = await self.client.audio.speech.create(
			input = text, 
			voice = 'nova', 
			model = 'tts-1'
		)

		response.stream_to_file(path)

	async def search(self, query: str) -> str:

		await self.setup_event.wait()

		message = await self.client.beta.threads.messages.create(
			thread_id = self.thread.id,
            role = 'user',
            content = query
		)

		run = await self.client.beta.threads.runs.create(
			thread_id = self.thread.id,
			assistant_id = self.assistant.id
		)

		while run.status not in ['completed', 'failed']:

			await asyncio.sleep(1)
			run = await self.client.beta.threads.runs.retrieve(
				thread_id = self.thread.id,
				run_id = run.id
			)

		content = None

		if run.status == 'completed':

			messages = await self.client.beta.threads.messages.list(
				thread_id = self.thread.id
			)
			content = messages.data[0].content[0].text.value if messages else 'Server Error.'	

		else:

			content = run.status

		return content



class Bot():

	def __init__(self, openai_api_token: str, telegram_token: str):

		self.engine = Engine(openai_api_token)
		self.bot = aiogram.Bot(token = telegram_token)
		self.dispatcher = aiogram.Dispatcher()
		self.setup()


	def setup(self):

		@self.dispatcher.message(aiogram.F.text)
		async def handle_text_message(message: aiogram.types.Message):

			try:

				await self.bot.send_message(message.chat.id, 'Hi!')

			except Exception as exception:

				print('Oops!', exception)

		@self.dispatcher.message(aiogram.F.voice)
		async def handle_voice_message(message: aiogram.types.Message):

			try:

				voice_input_path = 'request.mp3'
				voice_output_path = 'response.mp3'

				voice_file_id = message.voice.file_id
				voice_file = await self.bot.get_file(voice_file_id)
				await self.bot.download_file(voice_file.file_path, voice_input_path)

				query = await self.engine.voice_to_text(voice_input_path)
				answer = await self.engine.search(query)
				await self.engine.text_to_voice(answer, voice_output_path)
				await self.bot.send_voice(message.chat.id, aiogram.types.FSInputFile(voice_output_path))

				os.remove(voice_input_path)
				os.remove(voice_output_path)

			except Exception as exception:

				print(exception)
				await self.bot.send_message(message.chat.id, 'Oops! Something is wrong.')

	async def run(self):

		await self.dispatcher.start_polling(self.bot)


if __name__ == '__main__':

	async def main():

		bot = Bot(settings.OPENAI_API_TOKEN.get_secret_value(), settings.TELEGRAM_TOKEN.get_secret_value())
		await bot.run()

	asyncio.run(main())


	