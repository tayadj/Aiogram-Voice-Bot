import aiogram



async def handle_photo_message(message: aiogram.types.Message, engine):

	try:

		photo_input_path = str(message.message_id) + '_photo_request.jpg'

		photo_file_id = message.photo[0].file_id
		photo_file = await message.bot.get_file(photo_file_id)
		await message.bot.download_file(photo_file.file_path, photo_input_path)

		answer = await engine.analyze_mood(photo_input_path)
		await message.bot.answer(answer)

		os.remove(photo_input_path)

	except Exception as exception:

		print(exception)
		await message.answer('Oops! Something is wrong.')