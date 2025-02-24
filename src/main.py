import asyncio
import openai
import pydantic_settings



class Settings(pydantic_settings.BaseSettings):
	
	model_config = pydantic_settings.SettingsConfigDict(
		env_file = '.env', env_file_encoding = 'utf-8', extra = 'ignore'
	)

	OPENAI_API_TOKEN: str
	TELEGRAM_TOKEN: str

settings = Settings()



class Engine():

	def __init__():

		pass