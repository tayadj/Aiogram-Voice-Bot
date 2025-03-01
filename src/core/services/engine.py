import aiogram
import asyncio
import json
import openai



class Engine():

	def __init__(self, openai_api_token: str, openai_api_assistant: str):

		self.client = openai.AsyncOpenAI(api_key = openai_api_token)

		self.assistant = None
		self.thread = None

		self.setup_event = asyncio.Event()
		asyncio.create_task(self.assistant_setup(openai_api_assistant))

	async def assistant_setup(self, openai_api_assistant: str):

		self.assistant = await self.client.beta.assistants.retrieve(openai_api_assistant)
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

		values = None

		message = await self.client.beta.threads.messages.create(
			thread_id = self.thread.id,
			role = 'user',
			content = query
		)

		run = await self.client.beta.threads.runs.create_and_poll(
			thread_id = self.thread.id,
			assistant_id = self.assistant.id
		)

		if run.status == 'completed':

			messages = await self.client.beta.threads.messages.list(
				thread_id = self.thread.id
			)
			content = messages.data[0].content[0].text.value if messages else 'Oops! Status: server_error'	

		elif run.status == 'requires_action':

			tool_responses = []

			for call in run.required_action.submit_tool_outputs.tool_calls:

				if call.function.name == 'analyze_value':

					print("call.function.arguments: ", call.function.arguments)
					arguments = json.loads(call.function.arguments)
					result = await self.validate_values(arguments['values'])
					
					tool_responses.append({
						'tool_call_id': call.id,
						'output': str(result)
					})

			await self.client.beta.threads.runs.submit_tool_outputs_and_poll(
				thread_id = self.thread.id,
				run_id = run.id,
				tool_outputs = tool_responses
			)

			messages = await self.client.beta.threads.messages.list(
				thread_id = self.thread.id
			)
			content = messages.data[0].content[0].text.value if messages else 'Oops! Status: server_error'	
			
		else:
			
			content = 'Oops! Status: ' + run.status

		return content, values

	async def validate_values(self, values) -> str:

		return True



		