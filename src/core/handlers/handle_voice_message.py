import os
import aiogram



async def handle_voice_message(message: aiogram.types.Message, engine):

    try:

        voice_input_path = str(message.message_id) + '_request.mp3'
        voice_output_path = str(message.message_id) + '_response.mp3'

        voice_file_id = message.voice.file_id
        voice_file = await message.bot.get_file(voice_file_id)
        await message.bot.download_file(voice_file.file_path, voice_input_path)

        query = await engine.voice_to_text(voice_input_path)
        answer = await engine.search(query)
        await engine.text_to_voice(answer, voice_output_path)

        await message.bot.send_voice(message.chat.id, aiogram.types.FSInputFile(voice_output_path))

        os.remove(voice_input_path)
        os.remove(voice_output_path)

    except Exception as exception:

        await message.answer('Oops! Something is wrong.')