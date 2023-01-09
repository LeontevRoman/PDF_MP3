from gtts import gTTS
import pdfplumber
from pathlib import Path

def converted(pages, file_path, language='ru'):
    print(f'[+] Original file: {Path(file_path).name}') #служебное сообщение
    print('[+] Processing...') #служебное сообщение

    text = ''.join(pages)
    text = text.replace('\n', '')

    my_audio = gTTS(text=text, lang=language)
    file_name = Path(file_path).stem

    my_audio.save(f'./result_MP3_files/{file_name}.mp3')
    return f'{file_name}.mp3'


def pdf_to_mp3(file_path='', language='ru'):
    """
    :param file_path:
    :param language: язык файла (пока не работает)
    :return: экземпляр объекта готового файла с именем и путь до него
    """
    with pdfplumber.PDF(open(file_path, mode='rb')) as pdf:
        all_pages_text = [page.extract_text() for page in pdf.pages]
    return converted(all_pages_text, file_path)



def txt_to_mp3(file_path='', language='ru'):
    #добавить кодировку файла пока временно не работает
    with open(file_path) as text:
        lines = [line for line in text]
    return converted(lines, file_path)


def main():
    print('PDF or TXT to MP3')
    file_name = input('\nPlease input file name: ')

    '''if Path(file_name).suffix == '.pdf':
        print(pdf_to_mp3(file_path='./downloads_files/'+file_name, language='ru'))
    elif Path(file_name).suffix == '.txt':
        print(txt_to_mp3(file_path='./downloads_files/' + file_name, language='ru'))
    else:
        print('File not exists! Check the file path...')'''


if __name__ == '__main__':
    main()