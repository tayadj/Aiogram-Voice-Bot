import aiogram
import asyncio
import base64
import json
import openai
import pydantic



class Engine():

	def __init__(self, openai_api_token: str, openai_api_assistant: str, openai_api_vectorstore: str):

		self.client = openai.AsyncOpenAI(api_key = openai_api_token)

		self.vector_store = None
		self.assistant = None
		self.thread = None

		self.setup_event = asyncio.Event()
		asyncio.create_task(self.engine_setup(openai_api_assistant, openai_api_vectorstore))

	async def engine_setup(self, openai_api_assistant: str, openai_api_vectorstore: str):

		self.vector_store = await self.client.beta.vector_stores.retrieve(openai_api_vectorstore)
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

		async def postprocess(messages, status):

			content = ''

			if status not in ['completed', 'requires_action']:
			
				content = f'Oops! Status: {status}'

			else:

				message_content = messages.data[0].content[0].text
				annotations = message_content.annotations
				citations = []

				for index, annotation in enumerate(annotations):

					message_content.value = message_content.value.replace(annotation.text, f'[{index + 1}]')

					if file_citation := getattr(annotation, 'file_citation', None):

						cited_file = await self.client.files.retrieve(file_citation.file_id)
						citations.append(f'[{index + 1}] {cited_file.filename}')

				content = messages.data[0].content[0].text.value if messages else 'Oops! Status: server_error'
				content += '\n\n' + '\n'.join(citations)

			return content

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

		if run.status == 'requires_action':

			tool_responses = []

			for call in run.required_action.submit_tool_outputs.tool_calls:

				if call.function.name == 'analyze_value':

					arguments = json.loads(call.function.arguments)
					result = await self.validate_values(arguments['values'])

					if result.validated:

						values = arguments['values']
					
					tool_responses.append({
						'tool_call_id': call.id,
						'output': str(result.validated)
					})

			await self.client.beta.threads.runs.submit_tool_outputs_and_poll(
				thread_id = self.thread.id,
				run_id = run.id,
				tool_outputs = tool_responses
			)

		messages = await self.client.beta.threads.messages.list(
			thread_id = self.thread.id,
			run_id = run.id
		)
		content = await postprocess(messages, run.status)

		return content, values, {'thread_id': self.thread.id, 'run_id': run.id}

	async def validate_values(self, values):

		class Validation(pydantic.BaseModel):
		
			validated: bool

		completion = await self.client.beta.chat.completions.parse(
			model = 'gpt-4o-mini-2024-07-18',
			messages = [
				{'role': 'system', 'content': 'Determine whether the detection of user-defined moral values (in the format of comma-separated words) correct and free of nonsense.'},
				{'role': 'user', 'content': values}
			],
			response_format = Validation
		)

		response = completion.choices[0].message.parsed

		return response

	async def analyze_mood(self, path: str):

		def encode_image(path: str):

			with open(path, 'rb') as file:

				return base64.b64encode(file.read()).decode('utf-8')

		base64_image = encode_image(path)

		response = await self.client.chat.completions.create(
			model = 'gpt-4o-mini',
			messages = [
				{
					'role': 'user', 
					'content': [
						{
							'type': 'text', 
							'text': 'Determine the mood from the photo'
						},
						{
							'type': 'image_url',
							'image_url': {
								'url': f'data:image/jpeg;base64,{base64_image}'
							}                
						}
					]
				}
			]
		)

		return response.choices[0].message.content