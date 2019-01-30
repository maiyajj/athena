# -*- coding: utf-8 -*-
import logging

import requests
from rx import Observer

from src.core.models import ChatRoomMessage, Patterns
from src.core.settings import DEFAULT_REQUEST_HEADERS
from src.observables import stream, subscribe

logger = logging.getLogger(__name__)


class Obs(Observer):

    def handle(self, message):
        pass

    def on_next(self, value):
        try:
            self.handle(value)
        except Exception as e:
            logger.error(str(e), exc_info=True)

    def on_error(self, error):
        logger.error(str(error))

    def on_completed(self):
        pass


@subscribe(stream)
class MessageBackup(Obs):
    def handle(self, message: ChatRoomMessage):
        logger.info(f'{message.chatroom.value}-{message.nickname}:{message.text}')


@subscribe(stream.filter(lambda message: Patterns.why.match(message.text)))
class Why(Obs):
    def handle(self, message: ChatRoomMessage):
        message.reply('@{} 哪来那么多为什么，快干活去'.format(message.nickname))


@subscribe(stream.filter(lambda message: Patterns.url.match(message.text)))
class PreviewUrl(Obs):
    def handle(self, message: ChatRoomMessage):
        url = Patterns.url.match(message.text).group(1)
        response = requests.get(url, headers=DEFAULT_REQUEST_HEADERS)
        if response.status_code != 200:
            return
        content_type = response.headers.get('Content-Type', '').lower()
        if content_type.startswith('text/html'):
            match = Patterns.html_title.search(response.text)
            if not match:
                return
            title = match.groups()[0]
            return message.reply(f'网址：{url}\n标题：{title}')
        elif content_type.startswith('application/json'):
            return message.reply(response.text)
