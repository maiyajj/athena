# -*- coding: utf-8 -*-
import logging

from rx.subjects import Subject

from src.core.models import ChatRoomMessage

logger = logging.getLogger(__name__)

# 收到微信的原始 dict 数据
raw_stream = Subject()

# 收指定微信群的数据
stream = raw_stream.map(lambda message: ChatRoomMessage(message)).filter(lambda message: message.chatroom)


def subscribe(observable):
    """ 订阅装饰器，cls订阅observable """

    def wrapper(cls):
        observable.subscribe(cls())
        return cls

    return wrapper


def no_exception(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(str(e), exc_info=True)

    return wrapper
