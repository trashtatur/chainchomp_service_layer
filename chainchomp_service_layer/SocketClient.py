from typing import Callable

import socketio
from chainchomplib import LoggerInterface
from chainchomplib.adapterlayer.MessageDeserializer import MessageDeserializer
from chainchomplib.configlayer.model.ChainfileModel import ChainfileModel
from chainchomplib.data import SocketEvents

from chainchomp_service_layer.SocketEmitter import SocketEmitter


class SocketClient:
    def __init__(self):
        self.sio = socketio.AsyncClient()
        self.URL = 'http://localhost:4410'
        self.socket_emitter = SocketEmitter(self.sio)
        self.using_chainlink: ChainfileModel or None = None
        self.service_callback = None
        self.sio.on(SocketEvents.EMIT_TO_APPLICATION, self.on_receive_message)

    async def on_receive_message(self, data):
        if self.service_callback is None:
            LoggerInterface.error(f'You need to call set_up on the ServiceLayerInterface before you start sending!')
            return

        message = MessageDeserializer.deserialize(data)
        if message is not None:
            self.service_callback(
                message.message_body,
                message.message_header.origin,
                message.message_header.adapter_name
            )
        else:
            LoggerInterface.error(f'A received data package was not properly formatted. It will be ignored')

    async def connect(self):
        if self.using_chainlink is None:
            LoggerInterface.error(f'You need to call set_up on the ServiceLayerInterface before you connect!')
            return
        await self.sio.connect(self.URL, headers={'CHAINLINK_NAME': self.using_chainlink.chainlink_name})
        await self.sio.wait()

    def set_callback(self, callback_function: Callable):
        self.service_callback = callback_function

    def set_using_chainlink(self, chainlink: ChainfileModel):
        self.using_chainlink = chainlink


