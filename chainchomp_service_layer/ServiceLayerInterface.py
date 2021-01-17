import asyncio
from typing import Callable, Generic, TypeVar

from chainchomplib import LoggerInterface
from chainchomplib.adapterlayer.Message import Message
from chainchomplib.adapterlayer.MessageHeader import MessageHeader
from chainchomplib.configlayer.ChainlinkResolver import ChainlinkResolver

from chainchomp_service_layer.SocketClient import SocketClient

client = SocketClient()
T = TypeVar('T')


def emit(message: Generic[T]) -> T or None:
    """
    Emits a message to chainchomps core. You need to call set_up first before this will work.
    If it is not set up, it will just return your message and write an error message into
    the logs.
    :param message: A data package that you want to send off. Chainchomp takes care of all the formatting.
    :return: Either your message or None if successful
    """
    emitter = client.socket_emitter
    if client.using_chainlink is None:
        LoggerInterface.error('Call the setup function successfully first before you emit')
        return message
    chainlink_name = client.using_chainlink.chainlink_name
    adapter = client.using_chainlink.adapter
    next_links = client.using_chainlink.next_links
    message = Message(message, MessageHeader(chainlink_name, next_links, adapter))
    emitter.emit_to_chainchomp_core(message.get_serialized())


def set_up(name: str, callback: Callable[[str, str, str], ...]):
    """
    This function sets up the connection to chainchomp from your
    application. It is imperative that it is called before any sending takes place.

    :param name: The name of your chainlink. It will be resolved to the chainfile of your chainlink if
    that chainlink is registered.
    :param callback: A callback function. It is called when a message arrives. It is expect to accept 3 parameters
    The first is the message body. The second is the message origin and the second is the adapter that was used
    to send it. Your function does not need to consume all these arguments, but should provide them in its signature.
    :return: None
    """
    if name is None:
        LoggerInterface.error('Provided name can not be None')
        return
    if not callable(callback):
        LoggerInterface.error('Provided callback must be callable')
        return

    chainlink_model = ChainlinkResolver.resolve(name)
    if chainlink_model is None:
        LoggerInterface.error(f'The chainlink {name} is not registered yet. Register it first!')
        return

    client.set_callback(callback)
    client.set_using_chainlink(chainlink_model)
    loop = asyncio.get_event_loop()
    loop.create_task(client.connect())
    loop.run_forever()
