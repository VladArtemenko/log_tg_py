import datetime
import os
import requests


class TelegramLog:
    url = "https://api.telegram.org/bot"

    def __init__(self, token, chat_id, script_name):
        self.user_name = os.environ.get("USERNAME")
        self.url += token
        self.chat_id = chat_id
        self.script_name = script_name

    def send_message(self, level, text):
        send_message_url = self.url + '/sendMessage'

        if level != 'info':
            notification = False
        else:
            notification = True

        post = requests.post(
            send_message_url,
            data={
                "chat_id": self.chat_id,
                "text": text,
                "parse_mode": 'Markdown',
                "disable_notification": notification
            }
        )
        print(post.text)
        if post.status_code != 200:
            print(f"Не могу отправить лог, время ошибки = {str(datetime.datetime.now())[:-7]}")

    def create_log(self, level, text):
        return f"""
*Дата:* `{str(datetime.datetime.now())[:-7]}`
*Логин:* `{self.user_name}`
*Скрипт:* `{self.script_name}`
*Уровень лога:* `{level}`
`{text}`
        """

    def info(self, text):
        self.send_message(
            "info",
            self.create_log('info', text)
        )

    def warning(self, text):
        self.send_message(
            "waring",
            self.create_log('warning', text)
        )

    def critical(self, text):
        self.send_message(
            "critical",
            self.create_log('critical', text)
        )


log = TelegramLog(
    token='5259727067:AAFjDk_HOdbg8LoT7Is5XS6kiGyv2TrcE98',
    chat_id='-1001779836149',
    script_name='test'
)

log.warning("что-то жуткое произошло")