import asyncio
import unittest
from unittest.mock import MagicMock

import socketio
from chainchomplib.adapterlayer.Message import Message
from chainchomplib.adapterlayer.MessageHeader import MessageHeader

from chainchomp_service_layer.service_layer.SocketClient import SocketClient


class SocketClientTest(unittest.TestCase):

    def test_that_the_callback_gets_called_correctly(self):
        uut = self.get_unit_under_test()
        uut.set_callback(self.callback)
        self._run()
        self._origin.assert_called_once()
        self._body.assert_called_once()
        self._adapter_name.assert_called_once()

    def get_unit_under_test(self) -> SocketClient:
        sio_mock = socketio.AsyncClient()
        sio_mock.on = MagicMock(return_value=None)
        self._body = MagicMock(return_value=None)
        self._origin = MagicMock(return_value=None)
        self._adapter_name = MagicMock(return_value=None)
        return SocketClient(sio_mock)

    def _run(self):
        uut = self.get_unit_under_test()
        uut.set_callback(self.callback)
        return asyncio.get_event_loop().run_until_complete(uut.on_receive_message(
            Message(
                'test',
                MessageHeader('test_link', ['one'], 'test_adapter')
            ).get_serialized()
        ))

    def callback(self, body, origin, adapter_name):
        if body:
            self._body()
        if origin:
            self._origin()
        if adapter_name:
            self._adapter_name()

