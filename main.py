import time
from sys import path_hooks

from models.telegram import SendMessage
from utils.wrapper.telegram import TelegramBot


def main():
    bot = TelegramBot()
    bot.send_message(message=SendMessage(text='Initiates'))
    while True:
        message = bot.get_latest_response()
        if message:
            if message.text:
                print(message.text)
            elif message.photo:
                photo = message.photo[-1]
                bot.get_file_object(photo.file_id)

        time.sleep(0.5)

    pass


if __name__ == '__main__':
    main()
