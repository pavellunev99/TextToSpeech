import telebot
import pyttsx3
import os
from pydub import AudioSegment

bot = telebot.TeleBot('1845322686:AAFytbyICZH76cz2SRYQ6l94XTvA8kZQA7M')
fileName = "voice.ogg"
fullPath = os.path.join(os.getcwd(), fileName)

def change_voice(engine, language, gender= 'VoiceGenderFemale'):
    for voice in engine.getProperty('voices'):
        if language in voice.languages and gender == voice.gender:
            engine.setProperty('voice', voice.id)
            return True

    raise RuntimeError("Language '{}' for gender '{}' not found".format(language, gender))

def engine_settings(engine):
    voices = engine.getProperty('voices')
    engine.setProperty('rate', 185)  # Выставляем скорость чтения голоса
    change_voice(engine, "ru_RU", "VoiceGenderFemale")

def get_mp3_file(text):
    engine = pyttsx3.init()
    #engine_settings(engine)  # Применение настроек голоса
    engine.save_to_file(text, fullPath)  # Сохранение сообщения в аудиофайл
    engine.runAndWait()
    #convert_file_to_ogg('voice.ogg')  # Конвертация

def convert_file_to_ogg():
    converter = AudioSegment
    converter_file = converter.from_file(fullPath)
    converter_file.export(fullPath, format="ogg")

@bot.message_handler(commands=['start'])
def forward_message(message):
    bot.send_message(message.from_user.id, "Привет, я голосовой бот для курсовой")

@bot.message_handler(content_types=['text'])
def forward_message(message):
    f = open(fullPath, 'rb')
    get_mp3_file(message)
    bot.send_audio(message.from_user.id, audio=f)
    f.close()

bot.polling()