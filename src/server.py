# -*- coding: utf-8 -*-
import itchat

from src.core.models import ChatRooms
from src.core.storage import Storage, MemoryStorage
from src.observables import raw_stream
from itchat.storage.messagequeue import Message  # 支持attr操作的字典


@itchat.msg_register(itchat.content.TEXT, isGroupChat=True)
def handle_group_message(message: Message):
    print(message)
    raw_stream.on_next(message)


def run_server():
    print("starting")
    itchat.auto_login(enableCmdQR=2, hotReload=True)
    ChatRooms.load_chatroom()
    with Storage(MemoryStorage) as storage:
        print(storage.get('chatroom_map', {}))
    itchat.run()
