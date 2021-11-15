import typing
from typing import Optional
from numpy import random, int32

import aiohttp
from aiohttp.client import ClientSession

from app.base.base_accessor import BaseAccessor
from app.store.vk_api.dataclasses import Message, Update, UpdateMessage, UpdateObject
from app.store.vk_api.poller import Poller

if typing.TYPE_CHECKING:
    from app.web.app import Application


class VkApiAccessor(BaseAccessor):
    def __init__(self, app: "Application", *args, **kwargs):
        super().__init__(app, *args, **kwargs)
        self.session: Optional[ClientSession] = None
        self.key: Optional[str] = None
        self.server: Optional[str] = None
        self.poller: Optional[Poller] = None
        self.ts: Optional[int] = None

    async def connect(self, app: "Application"):
        self.app = app
        self.session = aiohttp.ClientSession(raise_for_status=True)
        # TODO: добавить создание aiohttp ClientSession,
        #  получить данные о long poll сервере с помощью метода groups.getLongPollServer
        #  вызвать метод start у Poller
        server_response = await self._get_long_poll_service()

        self.server = server_response['server']
        self.key = server_response['key']
        self.ts = server_response['ts']
        self.poller = Poller(store=self.app.store)

        await self.poller.start()

        # await self.poll()

    async def disconnect(self, app: "Application"):
        # TODO: закрыть сессию и завершить поллер
        self.app = None
        if self.session is not None:
            await self.session.close()

    @staticmethod
    def _build_query(host: str, method: str, params: dict) -> str:
        url = host + method + "?"
        if "v" not in params:
            params["v"] = "5.131"
        url += "&".join([f"{k}={v}" for k, v in params.items()])
        return url

    async def _get_long_poll_service(self):
        host = 'https://api.vk.com/'
        method = 'method/groups.getLongPollServer'
        params = {
            'group_id': self.app.config.bot.group_id,
            'access_token': self.app.config.bot.token,
            'v': 5.131,
        }

        url = self._build_query(host, method, params)

        response = await self.session.get(url)
        server_params = await response.json()
        return server_params['response']

    async def poll(self):
        url = f'{self.server}?act=a_check&key={self.key}&ts={self.ts}&wait=10'
        self.ts = int(self.ts) + 1
        request = await self.session.get(url)
        api_response = await request.json()
        update = Update(type='None', object=UpdateObject(message=UpdateMessage(from_id=0, text='No updates to handle', id=0)))
        if 'updates' in api_response and api_response['updates']:
            if api_response['updates'][0]['type'] == 'message_new':
                update_message = UpdateMessage(from_id=api_response['updates'][0]['object']['message']['from_id'],
                                               text=api_response['updates'][0]['object']['message']['text'],
                                               id=api_response['updates'][0]['object']['message']['id'])
                update_object = UpdateObject(message=update_message)
                update = Update(type=api_response['updates'][0]['type'], object=update_object)


        else:
            url = f'{self.server}?act=a_check&key={self.key}&ts={self.ts + 1}&wait=5'
            await self.session.get(url)


        return update

    async def send_message(self, message: Message) -> None:
        host = 'https://api.vk.com/'
        method = 'method/messages.send'
        params = {
            'user_id': message.user_id,
            'message': message.text,
            'random_id': random.randint(2147483647, size=1, dtype=int32)[0],
            'access_token': self.app.config.bot.token,
            'v': 5.131,
        }

        url = self._build_query(host, method, params)
        await self.session.post(url)
