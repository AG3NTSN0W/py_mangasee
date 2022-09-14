import requests
from utils.logger import logger
from repository.notification_DB import Notifications


class Notification():

    def send(self, chapter: str):
        for toSend in Notifications().get_notification():
            self.sendTo(toSend.to_tuple(), chapter)

    @staticmethod
    def sendTo(sendTo, chapter) -> bool:
        (_, type, token, chatId) = sendTo
        if (type == 'telegram'):
            return TelegramNotification().send((token, chatId, chapter))


class TelegramNotification():

    url = "https://api.telegram.org/bot{token}/sendMessage"

    text = "Manga Downloaded \n{chapter}"

    data = {
        "chat_id": "<<Place holder>>",
        "text": "<<Place holder>>",
        "disable_notification": True,
        "entities": [
            {
                "type": "bold",
                "offset": 0,
                "length": 16
            }
        ]
    }

    def send(self, send: tuple) -> bool:
        try:
            logger.info(f"Notification to Send: {send}")
            (token, chatId, chapter) = send
            data = self.data
            data['chat_id'] = chatId
            data['text'] = self.text.format(chapter=chapter)
            logger.info(f"Notification to Send Data: {data}")
            r = requests.post(self.url.format(token=token), data=data)
            if (r.status_code == requests.codes.ok):
                logger.info("Telegram notification Send")
                return True
            logger.error(f"Failed to send telegram notification")
            return False
        except Exception as e:
            logger.error(f"Error Sending Telegram notification: {e}")
            return False
        pass
