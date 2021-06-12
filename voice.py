import pyttsx3
from pydub import AudioSegment
import re


def engine_settings(engine, article_language):
    voices = engine.getProperty('voices')
    engine.setProperty('rate', 185)  # Выставляем скорость чтения голоса
    for voice in voices:
        if voice.languages == article_language and \
                voice.gender == 'VoiceGenderMale':
            return engine.setProperty('voice', voice.id)  # Выбираем подходящий голос


def get_mp3_file(file_name, article_text, article_language):
    engine = pyttsx3.init()
    engine_settings(engine, article_language)  # Применение настроек голоса
    engine.save_to_file(article_text, file_name)  # Сохранение текста статьи в аудиофайл
    engine.runAndWait()
    convert_file_to_mp3(file_name)  # Конвертация в mp3 формат


def convert_file_to_mp3(file_name):
    converter = AudioSegment
    converter_file = converter.from_file(file_name)
    converter_file.export(file_name, format="mp3")


def get_file_name(link):
    # Название файла - ссылка на статью
    file_name = re.split(r'^https?:\/\/?', link)[1]
    for symbols_in_file_name in ['/', '.', '-']:
      # Замена символов в названии файла на '_', чтобы сохранить файл в OS
        file_name = file_name.replace(symbols_in_file_name, '_')
    file_name = file_name+'.mp3'  # Сохраняем файл изначально в mp3 формате
    return file_name