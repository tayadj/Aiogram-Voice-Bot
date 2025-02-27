import aiogram

async def handle_voice_message(message: aiogram.types.Message):

	try:

	#UNIQUE FILE NAMES

		voice_input_path = 'request.mp3'
		voice_output_path = 'response.mp3'

		voice_file_id = message.voice.file_id
		voice_file = await self.bot.get_file(voice_file_id)
		await self.bot.download_file(voice_file.file_path, voice_input_path)

		query = await self.engine.voice_to_text(voice_input_path)
		answer = await self.engine.search(query)
		await self.engine.text_to_voice(answer, voice_output_path)
		await self.bot.send_voice(message.chat.id, aiogram.types.FSInputFile(voice_output_path))

		os.remove(voice_input_path)
		os.remove(voice_output_path)

	except Exception as exception:

		print(exception)
		await self.bot.send_message(message.chat.id, 'Oops! Something is wrong.')