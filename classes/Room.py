import uuid

from aiogram.types import Message, FSInputFile
from aiogram import Bot


class Room:
    def __init__(self, owner_id, Password):
        unic_id = uuid.uuid1()
        self.data = {
            "uid": unic_id,
            "users": [owner_id],
            "owner": owner_id,
            "banned": [],
        }
        self.State = "Prepare"

    def send_to_all_players(
        self,
        bot: Bot,
        message: Message,
        photo: FSInputFile = None,
        ignoreSender: bool = False,
    ) -> None:
        if not (photo is None) or not (photo is "") and photo is FSInputFile:
            message = lambda user: bot.send_photo(
                user, photo, caption=message.text
            )
        else:
            message = lambda user: bot.send_message(user, text=message.text)

        if ignoreSender:
            users = self.data["users"].remove(
                message.chat.id
            )  # Берём список всех игроков в комнате и удаляем из него отправителя
        else:
            users = self.data["users"]

        for user in users:
            message(user)
