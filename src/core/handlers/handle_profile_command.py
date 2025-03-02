import aiogram



async def handle_profile_command(message: aiogram.types.Message, database):

	try:

		async with database.session_local() as session:
	
			user = await database.model_user.read_user(session, message.from_user.id)
		
			await message.answer(f'Profile\n\nValues: {user.values}')

	except Exception as exception:

		print(exception)
		await message.answer('Oops! Something is wrong.')