import telebot
import pyttsx3
from pydub import AudioSegment

bot = telebot.TeleBot('1845322686:AAFytbyICZH76cz2SRYQ6l94XTvA8kZQA7M')

def change_voice(engine, language, gender='VoiceGenderFemale'):
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
    engine_settings(engine)  # Применение настроек голоса
    engine.save_to_file(text, 'voice.ogg')  # Сохранение сообщения в аудиофайл
    engine.runAndWait()
    convert_file_to_ogg('voice.ogg')  # Конвертация

def convert_file_to_ogg(file_name):
    converter = AudioSegment
    converter_file = converter.from_file(file_name)
    converter_file.export(file_name, format="ogg")

@bot.message_handler(commands=['start'])
def forward_message(message):
    bot.send_message(message.from_user.id, "Привет, я голосовой бот для курсовой")

@bot.message_handler(content_types=['text'])
def forward_message(message):
    get_mp3_file(message)
    bot.send_audio(message.from_user.id, audio=open('voice.ogg', 'rb'))

bot.polling()