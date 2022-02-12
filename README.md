# Логгирование работы скриптов с помощью ТГ бота.

В данном репозитории хранится файл tg_log.py который позволяет логгировать работу скриптов на подобии библиотеки logging. 

## Инициализация библиотеки. 
Для инициализации логгирования нужно поместить tg_log.py в папку с основным кодом и прописать внутри кода следующие команды:

``` Python
import tg_log

TOKEN = <Ваш токен от тг бота>
CHAT_ID = <айди чата, куда бот должен отправлять сообщения> 
SCRIPT_NAME = <Название вашего скрипта>

logger = TelegramLog(
  TOKEN,
  CHAT_ID,
  SCRIPT_NAME,
  "%text"
)
```

## Как происходит логгирование
Все логи поделены на три уровня:
1. info
2. warning 
3. critical
Пока отличие между ними заключается лишь в том, что логи уровня info направляются с "бесшумным" уведомлением в телеграмме

# Обработка сообщений в ТГ с помощью данной библиотеки. 

На текущий момент обработка сообщений реализована только с функцией "Эхо" для текстовых сообщений. Логика следующая:
-- Внутри класса TelegramLog есть класс Filters, в котором есть функции, обрабатывающие входящие сообщения и возвращающие булево значение
-- Внутри класса TelegramLog есть класс BotLogic, в котором есть функции, обрабатывающие входящие сообщения и совершающие заданные действия
-- Если срабатывает фильтр, то запускается определенная функция

Пример:
``` Python
import tg_log

TOKEN = <Ваш токен от тг бота>
CHAT_ID = <айди чата, куда бот должен отправлять сообщения> 
SCRIPT_NAME = <Название вашего скрипта>

logger = TelegramLog(
  TOKEN,
  CHAT_ID,
  SCRIPT_NAME,
  "%text"
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
```