# -*- coding: utf-8 -*-
import logging

logger = logging.getLogger(__name__)


class MemoryStorage(object):
    __memory_dict = {}

    def get(self, key, default=None):
        return self.__memory_dict.get(key, default)

    def set(self, key, value):
        self.__memory_dict[key] = value
        return self

    def pop(self, key):
        if self.__memory_dict.get(key, False):
            self.__memory_dict.pop(key)

    def clear(self):
        self.__memory_dict.clear()


class FileStorage(object):
    pass


class Storage(object):
    def __init__(self, inner_storage=FileStorage):
        self.storage = inner_storage()

    def __enter__(self):
        return self.storage

    def __exit__(self, exc_type, exc_value, traceback):
        logger.info(f'exception_type: {exc_type}, exception_value: {exc_value}, traceback: {traceback}')
