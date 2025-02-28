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
	OPENAI_API_ASSISTANT: pydantic.SecretStr # VOICE_ASSISTANT
	# OPENAI_API_VALUE_ASSISTANT
	TELEGRAM_TOKEN: pydantic.SecretStr
	POSTGRE_URL: pydantic.SecretStr
