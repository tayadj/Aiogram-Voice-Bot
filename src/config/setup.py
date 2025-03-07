import openai


async def setup(openai_api_token: str):

	client = openai.AsyncOpenAI(api_key = openai_api_token)

	vector_store = await client.beta.vector_stores.create(
		name = 'Anxiety'
	)

	file = await client.files.create(
		file = open('Anxiety.docx', 'rb'),
		purpose = 'assistants'
	)

	vector_store_file = await self.client.beta.vector_stores.files.create(
		vector_store_id = openai_api_vectorstore,
		file_id = "file-Bu64hAV4S3QBUVWLRWr4Hp"
	)
	
	assistant = await client.beta.assistants.create(
		model = 'gpt-3.5-turbo',
		instructions = 'You are an assistant aimed to communicate with users, answer their messages and determine their moral values',
		tools = [
			{
				'type': 'function',
				'function': {
					'name': 'analyze_value',
					'description': 'Analyze user\'s message to determine key moral values.',
					'parameters': {
						'type': 'object',
						'properties': {
							'speech': {
								'type': 'string',
								'description': 'User\'s textual message'
							},
							'values': {
								'type': 'string',
								'description': 'User\'s key moral values in the form of a comma-separated list of words'
							}
						},
						'required': ['speech', 'values']
					}
				}
			},
			{
				'type': 'file_search'
			}
		],
		tool_resources = {
			'file_search': {
				'vector_store_ids': [
					vector_store.id
				]
			}
		}
	)

	print(f'Vector store info:\n{vector_store}\n\nAssistant info:\n{assistant}\n\nFile info:\n{file}\n\nVector store file info:\n{vector_store_file}')