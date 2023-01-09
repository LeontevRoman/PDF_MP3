from auth import TOKEN as token
from aiogram import Bot, Dispatcher, types, executor
from convert import txt_to_mp3, pdf_to_mp3
from pathlib import Path
import os

bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def start(message=types.Message):
    await bot.send_message(message.from_user.id,
                           f'Привет {message.from_user.first_name}! Я умею конвертировать .pdf ➡ .mp3!\n'
                           f'Просто отправь мне файл.')


@dp.message_handler(content_types='document')
async def converted(message=types.Message):

    file_suffix = Path(message.document.file_name).suffix

    if file_suffix not in ('.pdf', ):
        await message.answer('Sorry... The file format is unreadable!!!\nPlease send another file...')
    else:
        destination = f'./downloads_files/{message.document.file_name}'  # собираем нужный путь для сохранения
        await message.document.download(destination_file=destination)  # сохраняем документ
        print("[+] converted... Please wait") #служебный вывод в консоль
        await message.answer('[+] Converting.. Please wait...') #отправляем пользователю

        if file_suffix == '.pdf':
            result_file_name = pdf_to_mp3(destination, language='ru')  # отправляем файл на обработку и получаем новое имя файла

        '''elif file_suffix == '.txt': #посмотреть case
            result_file_name = txt_to_mp3(destination, language='ru') #отправляем файл на обработку и получаем новое имя файла '''


        print(f'[+] {result_file_name} SAVED!\nHave a good day!!!') #служебный вывод в консоль

        file = open(f'./result_MP3_files/{result_file_name}', 'rb')
        await message.answer_document(file, caption='DOWN! Have a good day!!!')

        os.remove(f'./downloads_files/{message.document.file_name}')
        os.remove(f'./result_MP3_files/{result_file_name}')

@dp.message_handler()
async def error(message=types.Message):
    await message.answer('Сообщения я не принимаю. Отправь файл формата .pdf или /start')


def main():
    print('Бот вышел в сеть...')
    executor.start_polling(dp)


if __name__ == '__main__':
    main()
