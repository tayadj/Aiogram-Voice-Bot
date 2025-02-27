import aiogram
import asyncio
import openai

class Engine():

	def __init__(self, openai_api_token: str):

		self.client = openai.AsyncOpenAI(api_key = openai_api_token)

		self.assistant = None
		self.thread = None

		self.setup_event = asyncio.Event()
		asyncio.create_task(self.assistant_setup())

	async def assistant_setup(self):

		#do not create, create in case if doesn't exist
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

		#create_and_poll

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