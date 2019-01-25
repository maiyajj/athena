# -*- coding: utf-8 -*-
import unittest

import fire

from src.server import run_server


class Manager(object):
    """project manager"""

    @staticmethod
    def server():
        run_server()

    @staticmethod
    def test():
        tests = unittest.defaultTestLoader.discover("src", "test*.py")
        test_runner = unittest.TextTestRunner()
        test_runner.run(tests)


if __name__ == "__main__":
    fire.Fire(Manager)
