import aiogram



async def handle_profile_command(message: aiogram.types.Message, engine, database):

	async with database.session_local() as session:
	
		user = await database.model_user.read_user(session, message.from_user.id)
		
		await message.answer(f'Profile\n\nValues: {user.values}')