import openai


async def setup(openai_api_token: str):

	client = openai.AsyncOpenAI(api_key = openai_api_token)

	vector_store = await client.beta.vector_stores.create(
		name = 'Anxiety'
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
			}
		]
	)

	print(f'Vector store info:\n{vector_store}\n\nAssistant info:\n{assistant}')