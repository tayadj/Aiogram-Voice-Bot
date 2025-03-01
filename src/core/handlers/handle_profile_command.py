import aiogram



async def handle_profile_command(message: aiogram.types.Message, engine, database):

	try:

		async with database.session_local() as session:
	
			user = await database.model_user.read_user(session, message.from_user.id)
		
			if user:
				
				await message.answer(f'Profile\n\nValues: {user.value}')					

			else:

				await message.answer('I don\'t know you yet.')
				await database.model_user.create_user(session, message.from_user.id, 'unknown')

	except Exception as exception:

		print(exception)
		await message.answer('Oops! Something is wrong.')