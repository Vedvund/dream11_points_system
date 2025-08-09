import json
import os.path
import time
from datetime import datetime, timedelta

import requests

from core.config import settings
from models.telegram import GetUpdatesResponse, SendMessage, SendFile, FileResult
from utils.helper.logger import setup_logging

logger = setup_logging()


class TelegramBot:
    # https://core.telegram.org/bots/api#available-methods
    def __init__(self):
        self.api_url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/"
        self.file_url = f"https://api.telegram.org/file/bot{settings.TELEGRAM_BOT_TOKEN}/"
        self.session = requests.Session()
        self.last_update_id = self._get_last_update_id()

    def _get_last_update_id(self):
        response = self.session.get(self.api_url + "getUpdates")
        response.raise_for_status()
        updates = GetUpdatesResponse.model_validate(response.json())
        return updates.result[-1].update_id if updates.result else 0

    def get_user_response(self):
        params = {"offset": self.last_update_id + 1, "limit": 1}
        response = self.session.get(self.api_url + "getUpdates", params=params)
        response.raise_for_status()
        updates = GetUpdatesResponse.model_validate(response.json())
        start_datetime = datetime.now()

        while datetime.now() - start_datetime < timedelta(minutes=2):
            if updates.result:
                self.last_update_id = updates.result[0].update_id
                return updates.result[0].message.text
            time.sleep(0.5)
            response = self.session.get(self.api_url + "getUpdates", params=params)
            updates = GetUpdatesResponse.model_validate(response.json())

        self.send_message(SendMessage(text="Haven't received any response from you"))
        return None

    def get_latest_response(self):
        params = {"offset": self.last_update_id + 1, "limit": 1}
        response = self.session.get(self.api_url + "getUpdates", params=params)
        response.raise_for_status()
        updates = GetUpdatesResponse.model_validate(response.json())

        if updates.result:
            self.last_update_id = updates.result[0].update_id
            return updates.result[0].message
        return None

    def get_file_object(self, file_id):
        # Get file metadata
        params = {"file_id": file_id}
        response = self.session.get(self.api_url + "getFile", params=params)
        response.raise_for_status()
        file_result = FileResult.model_validate(response.json()["result"])

        # Download file
        response = self.session.get(self.file_url + file_result.file_path)
        response.raise_for_status()

        # Save file locally
        file_path = os.path.join('scratchpad', 'telegram', os.path.basename(file_result.file_path))
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as file:
            file.write(response.content)

        return response.content

    def ask_user(self, message: SendMessage):
        self.send_message(message)
        return self.get_user_response()

    def send_keyboard_options(self, options, text="Select an option:"):
        keyboard = [[{"text": option}] for option in options]

        payload = {
            "chat_id": settings.TELEGRAM_DEFAULT_OWNER_ID,
            "text": text,
            "reply_markup": {"keyboard": keyboard, "resize_keyboard": False, "one_time_keyboard": True}
        }

        self.session.post(
            url=self.api_url + "sendMessage",
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload)
        )
        return self.get_user_response()

    def ask_yes_no(self, question):
        response = self.send_keyboard_options(options=["yes", "no"], text=question)
        return response == "yes"

    def send_message(self, message: SendMessage):
        try:
            response = self.session.post(f"{self.api_url}sendMessage", params=message.model_dump())
            response.raise_for_status()
            logger.info(f"Message sent successfully to {message.chat_id}")
        except Exception as e:
            logger.error(f"Error sending message: {str(e)}")

    def send_photo(self, telegram_file: SendFile):
        try:
            files = {'photo': telegram_file.file}
            params = telegram_file.model_dump(exclude={'file'})
            response = self.session.post(f"{self.api_url}sendPhoto", params=params, files=files)
            response.raise_for_status()
            logger.info(f"Photo sent successfully to {telegram_file.chat_id}")
        except Exception as e:
            logger.error(f"Error sending photo: {str(e)}")

    def send_document(self, telegram_file: SendFile):
        try:
            files = {'document': telegram_file.file}
            params = telegram_file.model_dump(exclude={'file'})
            response = self.session.post(f"{self.api_url}sendDocument", params=params, files=files)
            response.raise_for_status()
            logger.info(f"Document sent successfully to {telegram_file.chat_id}")
        except Exception as e:
            logger.error(f"Error sending document: {str(e)}")


if __name__ == "__main__":
    bot = TelegramBot()
    print(bot.ask_yes_no(question='Are you doing great?'))
