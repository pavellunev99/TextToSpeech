import telebot
import pyttsx3
import os
from pydub import AudioSegment

bot = telebot.TeleBot('1845322686:AAFytbyICZH76cz2SRYQ6l94XTvA8kZQA7M')
fileName = "voice.ogg"
engine = pyttsx3.init()

def engine_settings(engine):
    voices = engine.getProperty('voices')
    engine.setProperty('rate', 185)  # Выставляем скорость чтения голоса
    engine.setProperty('voice', 'com.apple.speech.synthesis.voice.milena.premium')

def convert_file_to_ogg():
    converter = AudioSegment
    converter_file = converter.from_file(fileName)
    converter_file.export(fileName, format="ogg")

@bot.message_handler(commands=['start'])
def forward_message(message):
    bot.send_message(message.from_user.id, "Привет, я голосовой бот для курсовой")

@bot.message_handler(content_types=['text'])
def forward_message(message):
    engine_settings(engine)  # Применение настроек голоса
    engine.save_to_file(message.text, fileName)  # Сохранение сообщения в аудиофайл
    engine.runAndWait()
    convert_file_to_ogg()  # Конвертация
    bot.send_audio(message.from_user.id, audio=open(fileName, 'rb'))

bot.polling()