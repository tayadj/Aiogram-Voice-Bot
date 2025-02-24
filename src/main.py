import asyncio

import openai
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

	def __init__(self, api_key: str):

		self.client = openai.AsyncOpenAI(api_key = api_key)

	async def voice_to_speech(self):

		pass

	async def speech_to_voice(self):

		pass

	async def search(self, query: str) -> str:

		response = await self.client.chat.completions.create(
			model = 'gpt-3.5-turbo',
			messages = [{'role': 'user', 'content': query}]
		)
		content = response.choices[0].message.content		

		return content



class Bot():

	pass



if __name__ == '__main__':

	engine = Engine(settings.OPENAI_API_TOKEN.get_secret_value())

	async def main():

		query = "Test query: what is the capital of France?"
		result = await engine.search(query)
		print(result)

	asyncio.run(main())