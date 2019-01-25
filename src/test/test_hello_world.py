# -*- coding: utf-8 -*-
from unittest import TestCase


class HelloWorldTest(TestCase):
    def test_hello_world(self):
        self.assertEqual("hello world", "hello world")
