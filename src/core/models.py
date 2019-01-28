# -*- coding: utf-8 -*-
import re
from enum import Enum

import itchat

from src.core.storage import Storage, MemoryStorage


class ChatRooms(Enum):
    SERVYOU_ROOMMATE = '这个名字真难看'
    SERVYOU_PARTNER = '啦啦啦啦啦啦'
    JUNIOR_HIGH_SCHOOL_PARTNER = '。我们一起走过的时光🌹'
    Athena_TEST_ROOM = 'Athena测试群'

    def __new__(cls, value):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.messages = []
        return obj

    @classmethod
    def get_from_name(cls, name) -> 'ChatRooms':
        for chatroom in cls:
            if name.startswith(chatroom.value):
                return chatroom

    @property
    def chatroom(self):
        with Storage(MemoryStorage) as storage:
            return storage.get('chatroom_map', {}).get(self)

    def send(self, text, image=False):
        if not text:
            return
        self.messages.append(text)
        if not self.chatroom:
            return
        if image:
            response = itchat.send_image(text, self.chatroom)
        else:
            response = itchat.send(text, self.chatroom)
        return response

    @classmethod
    def load_chatroom(cls):
        with Storage(MemoryStorage) as storage:
            if storage.get('chatroom_map', False):
                return
        chatrooms = itchat.get_chatrooms()
        chatroom_map = {}
        for chatroom in chatrooms:
            room = cls.get_from_name(chatroom.get('NickName', ''))
            if room:
                chatroom_map[room] = chatroom.get('UserName')
        with Storage(MemoryStorage) as storage:
            storage.set('chatroom_map', chatroom_map)


class Patterns(object):
    html_title = re.compile(r'<title[^>]*>([^<]+?)</title>')
    url = re.compile(r'(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)')
    why = re.compile(r'^.*[为什么].*$')


class ChatRoomMessage(object):
    def __init__(self, message_data):
        """
        :type message_data: dict
        """
        name = message_data.get('User', {}).get('NickName', '')
        self.raw_data = message_data
        self.chatroom = ChatRooms.get_from_name(name)  # 群聊
        self.username = str(message_data.get('ActualUserName', 'unknown'))  # 微信用户ID
        self.nickname = str(message_data.get('ActualNickName', ''))  # 微信用户昵称
        self.text = str(message_data.get('Text', '')).strip()  # 消息内容
        self.is_at = bool(message_data.get('IsAt', False))  # 是否是At消息
        self.replied = False  # 标记这条消息是否已回复

    def reply(self, text):
        if self.replied:
            return
        self.replied = True
        self.chatroom.send(str(text).strip())

    def set_text(self, text):
        self.text = text
        return self
