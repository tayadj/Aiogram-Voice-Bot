import aiogram

async def handle_text_message(message: aiogram.types.Message):

	try:

		await message.answer('Hi!')

	except Exception as exception:

		print('Oops!', exception)