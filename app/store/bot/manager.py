import typing

from app.store.vk_api.dataclasses import Update, Message

if typing.TYPE_CHECKING:
    from app.web.app import Application


class BotManager:
    def __init__(self, app: "Application"):
        self.app = app
        print(self.app)

    async def handle_updates(self, updates: list[Update]):
        update = updates[-1]
        if update.type == 'message_new':
            await self.app.store.vk.send_message(Message(user_id=update.object.message.from_id, text='Hello world!!!'))
            # await self. .store.vk.send_message(Message(user_id=update.object.message.from_id, text='Hello world!!!'))
        # raise NotImplementedError
