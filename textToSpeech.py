import requests, json, os, threading, pyttsx3, time

class TelegramBot:
    def __init__(self):
        self.__URL = 'https://api.telegram.org/bot1845322686:AAFytbyICZH76cz2SRYQ6l94XTvA8kZQA7M/'
        self.__last_update_id = 0
        self.__setLastUpdate()

    def runUpdate(self):
        threading.Timer(3.0, self.runUpdate).start()
        self.index()

    def generateVoice(self, text):
        engine = pyttsx3.init()

        # On linux make sure that 'espeak' and 'ffmpeg' are installed
        engine.save_to_file(text, 'voice.mp3')
        engine.set_voice("ru")
        engine.runAndWait()
        time.sleep(5)

    def __setLastUpdate(self):
        #not to send two responses
        response = requests.get(self.__URL + "getUpdates").json()
        result = response['result']
        if len(result) > 0:
            self.__last_update_id = result[len(result)-1]['update_id']

    def index(self):
        offset = self.__last_update_id + 1

        response = requests.get(self.__URL + "getUpdates?offset={offset}").json()
        result = response['result']

        if len(result) > 0:
            #respond to all new messages, and save the last update_id to the session
            for update in result:
                update_id = update['update_id']
                if(update_id > self.__last_update_id):
                    #line below should be here, otherwise bot sends us more than one replies,
                    # because code doesn't catch up with the logic sometimes
                    self.__last_update_id = update_id

                    message = update['message']
                    chat_id = message['chat']['id']
                    first_name = message['chat']['first_name']
                    username = message['chat']['username']

                    if("text" in message):
                        text            = message['text']
                        if(text == "/start"):
                            answer = "Привет {}, я голосовой бот созданный для курсовой".format(first_name)
                            requests.get('{}sendMessage?chat_id={}&text={}&parse_mode=HTML'.format(self.__URL, chat_id, answer))
                        else:
                            self.generateVoice(text)
                            files = {'voice': open('voice.mp3','rb')}
                            #send a voice message
                            print(requests.post('{}sendVoice?chat_id={}'.format(self.__URL, chat_id), files=files).json())
        return 0

telegramBot = TelegramBot()
telegramBot.runUpdate()
