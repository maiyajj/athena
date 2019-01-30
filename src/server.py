# -*- coding: utf-8 -*-
import itchat
from itchat.storage.messagequeue import Message  # 支持attr操作的字典

from src.core.models import ChatRooms
from src.observables import raw_stream


@itchat.msg_register(itchat.content.TEXT, isGroupChat=True)
def group_message(message: Message):
    raw_stream.on_next(message)


def run_server():
    print("starting")
    itchat.auto_login(enableCmdQR=2, hotReload=True)
    ChatRooms.load_chatroom()
    itchat.run()
