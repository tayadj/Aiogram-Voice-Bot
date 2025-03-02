import aiogram



async def handle_text_message(message: aiogram.types.Message):

	try:

		await message.answer('Please, talk to me via voice.')	

	except Exception as exception:

		await message.answer('Oops! Something is wrong.')