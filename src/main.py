import aiofiles
import aiogram
import asyncio
import openai
import pydantic
import pydantic_settings
import whisper



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

	async def voice_to_text(self, path: str) -> str:

		with open(path, 'rb') as voice_file:

			response = await self.client.audio.transcriptions.create(file = voice_file, model = 'whisper-1')

		return response.text

	async def text_to_voice(self, text: str, path: str):

		response = await self.client.audio.speech.create(input = text, voice = 'nova', model = 'tts-1')

		print(response)

		response.stream_to_file(path)

	async def search(self, query: str) -> str:

		response = await self.client.chat.completions.create(
			model = 'gpt-3.5-turbo',
			messages = [{'role': 'user', 'content': query}]
		)
		content = response.choices[0].message.content		

		return content



class Bot():

	def __init__(self, openai_api_token: str, telegram_token: str):

		self.engine = Engine(openai_api_token)
		
	async def process(self):

		voice_input = "query.mp3"
		voice_output = 'response.mp3'

		#query = await self.engine.voice_to_text(voice_input)
		#answer = await self.engine.search(query)
		#print(query, answer)
		answer = 'The capital of France is Paris'
		await self.engine.text_to_voice(answer, voice_output)
		


if __name__ == '__main__':

	bot = Bot(settings.OPENAI_API_TOKEN.get_secret_value(), settings.TELEGRAM_TOKEN.get_secret_value())
	asyncio.run(bot.process())
	