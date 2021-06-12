import telebot
from voice import get_mp3_file


bot = telebot.TeleBot('1845322686:AAFytbyICZH76cz2SRYQ6l94XTvA8kZQA7M')

@bot.message_handler(commands=['start'])
def forward_message(message):
    bot.send_message(message.from_user.id, "Привет, я голосовой бот для курсовой")

@bot.message_handler(content_types=['text'])
def forward_message(message):
    file_name = 'voice.mp3'
    get_mp3_file(file_name, message, 'ru_RU')
    bot.send_audio(message.from_user.id, audio=open(file_name, 'rb'))

bot.polling()