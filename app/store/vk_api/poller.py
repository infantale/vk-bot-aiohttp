import asyncio
import typing
from asyncio import Task
from typing import Optional

from app.store import Store
from app.store.bot.manager import BotManager


class Poller:

    def __init__(self, store: Store):
        self.store = store
        self.is_running = False
        self.poll_task: Optional[Task] = None

    async def start(self):
        # TODO: добавить asyncio Task на запуск poll
        self.is_running = True

        self.poll_task = asyncio.create_task(self.poll())
        # task = await self.poll_task
        # print('task=', task)

        # raise NotImplementedError

    async def stop(self):
        # TODO: gracefully завершить Poller
        raise NotImplementedError

    async def poll(self):
        updates = list()

        # update = await self.store.vk.poll()
        # updates.append(update)
        # await BotManager.handle_updates(self.store.vk.app, updates=updates)

        while self.is_running:
            update = await self.store.vk.poll()
            if update.type == 'message_new':
                updates.append(update)
                print(updates)
                await BotManager.handle_updates(self.store.bot_manager, updates=updates)
                await asyncio.sleep(5)

        # updates.append(await self.store.vk.poll())
        # print(await self.store.vk.poll())
        # raise NotImplementedError
