import datetime
import os
import requests
from accessify import protected


class TelegramLog:
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
    def send_message(self, level, text):
        send_message_url = self.url + '/sendMessage'

        if level != 'info':
            notification = False
        else:
            notification = True

        try:
            post = requests.post(
                send_message_url,
                data={
                    "chat_id": self.chat_id,
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