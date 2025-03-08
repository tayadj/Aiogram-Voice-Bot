import asyncio
import os
import pydantic
import pydantic_settings



class Settings(pydantic_settings.BaseSettings):
	
	model_config = pydantic_settings.SettingsConfigDict(
		env_file = os.path.dirname(__file__) + '/.env',
		env_file_encoding = 'utf-8',
		extra = 'ignore'
	)

	OPENAI_API_TOKEN: pydantic.SecretStr
	OPENAI_API_ASSISTANT: pydantic.SecretStr
	OPENAI_API_VECTORSTORE: pydantic.SecretStr
	TELEGRAM_TOKEN: pydantic.SecretStr
	AMPLITUDE_API_TOKEN: pydantic.SecretStr
	DATABASE_URL: pydantic.SecretStr
	REDIS_URL: pydantic.SecretStr
