import asyncio
import queue
from threading import Thread
from typing import Generic, TypeVar

from chainchomplib import LoggerInterface
from chainchomplib.adapterlayer.Message import Message
from chainchomplib.adapterlayer.MessageHeader import MessageHeader
from chainchomplib.configlayer.resolver.ChainlinkResolver import ChainlinkResolver

from chainchomp_service_layer.MessageSendWorker import MessageSendWorker
from chainchomp_service_layer.SocketClient import SocketClient

T = TypeVar('T')


class ConnectionThread(Thread):

    def __init__(self, name, callback):
        """
        :param name: The name of your chainlink. It will be resolved to the chainfile of your chainlink if
        that chainlink is registered.
        :param callback: A callback function. It is called when a message arrives. It is expect to accept 3 parameters
        The first is the message body. The second is the message origin and the second is the adapter that was used
        to send it. Your function does not need to consume all these arguments, but should provide them in its signature
        """
        super().__init__()
        self.name = name
        self.callback = callback
        self.queued_messages = queue.PriorityQueue()
        self.socket_client = SocketClient()
        self.message_send_worker = MessageSendWorker(self.queued_messages, self.socket_client.sio)

    def emit(self, message: Generic[T]) -> T or None:
        """
        Emits a message to chainchomps core. You need to call set_up first before this will work.
        If it is not set up, it will just return your message and write an error message into
        the logs.
        :param message: A data package that you want to send off. Chainchomp takes care of all the formatting.
        :return: Either your message or None if successful
        """
        if self.socket_client.using_chainlink is None:
            LoggerInterface.error('Setup has not concluded yet. Wait a bit.')
            return message
        chainlink_name = self.socket_client.using_chainlink.chainlink_name
        adapter = self.socket_client.using_chainlink.adapter
        next_links = self.socket_client.using_chainlink.next_links
        message = Message(message, MessageHeader(chainlink_name, next_links, adapter))
        self.queued_messages.put(message)

    def run(self):
        self.message_send_worker.start()
        asyncio.run(self.__initiate_connection())

    async def __initiate_connection(self):
        """
        This function sets up the connection to chainchomp from your
        application. It is imperative that it is called before any sending takes place.
        :return: None
        """
        if self.name is None:
            LoggerInterface.error('Provided name can not be None')
            return
        if not callable(self.callback):
            LoggerInterface.error('Provided callback must be callable')
            return

        chainlink_model = ChainlinkResolver.resolve(self.name)
        if chainlink_model is None:
            LoggerInterface.error(f'The chainlink {self.name} is not registered yet. Register it first!')
            return

        self.socket_client.set_callback(self.callback)
        self.socket_client.set_using_chainlink(chainlink_model)
        await self.socket_client.connect()
