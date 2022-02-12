import datetime
import os
import time

import requests
from accessify import protected


class TelegramLog:
    class Filters:
        def __init__(self, result):
            self.result = result

        @staticmethod
        def no_filter():
            return True

    class BotLogic:
        def __init__(self, result, token):
            self.result = result
            self.token = token

        def only_text_echo(self):
            message_from = self.result['message']['from']['id']
            text = self.result['message']['text']
            return TelegramLog(self.token, message_from, "", "%text").warning(text)

    url = "https://api.telegram.org/bot"
    log_format = """
<b>Дата:</b> <code>%time</code>
<b>Логин:</b> <code>%user_name</code>
<b>Скрипт:</b> <code>%script_name</code>
<b>Уровень лога:</b> <code>%level</code>

%text
"""

    def __init__(self, token, chat_id, script_name, log_format=None):
        self.user_name = os.environ.get("USERNAME")
        self.url += token
        self.chat_id = chat_id
        self.script_name = script_name
        if log_format is not None:
            self.log_format = log_format

    @protected
    def send_message(self, level, text, chat_id=None):
        if chat_id is None:
            chat_id = self.chat_id

        send_message_url = self.url + '/sendMessage'

        if level != 'info':
            notification = False
        else:
            notification = True

        try:
            post = requests.post(
                send_message_url,
                data={
                    "chat_id": chat_id,
                    "text": text,
                    "parse_mode": 'HTML',
                    "disable_notification": notification
                }
            )
        except:
            text = f"Не могу отправить лог, время ошибки = {str(datetime.datetime.now())[:-7]}"
            print(text)
            try:
                requests.post(send_message_url, data={"text": text})
            except:
                print("Сообщение об ошибке также не смогли отправить")

        if post.status_code != 200:
            text = f"TG API status code 200 {str(datetime.datetime.now())[:-7]}"
            print(post.text)
            try:
                requests.post(send_message_url, data={"text": text})
            except:
                print("Сообщение об ошибке также не смогли отправить")
        return post.status_code

    @protected
    def create_log(self, level, text):
        dict_for_replace = {
            '%time': str(datetime.datetime.now())[:-7],
            '%user_name': self.user_name,
            '%script_name': self.script_name,
            '%level': level,
            '%text': text
        }
        current_msg = self.log_format
        for key in dict_for_replace:
            current_msg = current_msg.replace(key, dict_for_replace[key])
        return current_msg

    @protected
    def send_document(self, level, text, file):
        send_message_url = self.url + '/sendDocument'

        if level != 'info':
            notification = False
        else:
            notification = True

        try:
            post = requests.post(
                send_message_url,
                data={
                    "chat_id": self.chat_id,
                    "caption": text,
                    "parse_mode": 'HTML',
                    "disable_notification": notification
                },
                files={
                    'document': open(file, 'rb')
                }
            )
        except:
            text = f"Не могу отправить лог, время ошибки = {str(datetime.datetime.now())[:-7]}"
            print(text)
            try:
                requests.post(send_message_url, data={"text": text})
            except:
                print("Сообщение об ошибке также не смогли отправить")

        if post.status_code != 200:
            text = f"TG API status code 200 {str(datetime.datetime.now())[:-7]}"
            print(post.text)
            try:
                requests.post(send_message_url, data={"text": text})
            except:
                print("Сообщение об ошибке также не смогли отправить")
        return post.status_code

    def info(self, text, file=None):
        if file is None:
            self.send_message(
                "info",
                self.create_log('info', text)
            )
        else:
            self.send_document(
                "critical",
                self.create_log('critical', text),
                file
            )

    def warning(self, text, file=None):
        if file is None:
            self.send_message(
                "warning",
                self.create_log('warning', text)
            )
        else:
            self.send_document(
                "critical",
                self.create_log('critical', text),
                file
            )

    def critical(self, text, file=None):
        if file is None:
            self.send_message(
                "critical",
                self.create_log('critical', text)
            )
        else:
            self.send_document(
                "critical",
                self.create_log('critical', text),
                file
            )

    def get_updates(self, update_id):
        get_updates_url = self.url + '/getUpdates'
        return requests.post(
            get_updates_url,
            data={
                'offset': update_id + 1,
                'limit': 1,
                'timeout': 0
            }
        )


TOKEN = ''

logger = TelegramLog(
    TOKEN,
    '476973273',
    'echo',
    log_format="%text"
)


update_id = 0
while True:
    try:
        time.sleep(1)
        updates = logger.get_updates(update_id).json()
        if not updates['result']:
            continue

        update_id = updates['result'][0]['update_id']
        for update in updates['result']:
            if logger.Filters(update).no_filter():
                print(update)
                logger.BotLogic(update, TOKEN).only_text_echo()
    except Exception as e:
        print(e)
        break
