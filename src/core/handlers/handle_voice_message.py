import aiogram
import os



async def handle_voice_message(message: aiogram.types.Message, engine, database):

	try:

		voice_input_path = str(message.message_id) + '_request.mp3'
		voice_output_path = str(message.message_id) + '_response.mp3'

		voice_file_id = message.voice.file_id
		voice_file = await message.bot.get_file(voice_file_id)
		await message.bot.download_file(voice_file.file_path, voice_input_path)

		query = await engine.voice_to_text(voice_input_path)
		answer, value = await engine.search(query)
		await engine.text_to_voice(answer, voice_output_path)

		await message.bot.send_voice(message.chat.id, aiogram.types.FSInputFile(voice_output_path))

		os.remove(voice_input_path)
		os.remove(voice_output_path)

		if value:

			await message.answer(f'It seems like your moral value: {value}')
			
			async with database.session_local() as session:

				user = await database.model_user.update_user(session, message.from_user.id, value)
				print(user)

		else:

			await message.answer(f'I couldn\'t recognize your values for now')


	except Exception as exception:

		print(exception)
		await message.answer('Oops! Something is wrong.')