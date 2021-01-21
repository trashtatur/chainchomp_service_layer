from queue import PriorityQueue, Empty
from threading import Thread
from time import sleep

from chainchomplib import LoggerInterface
from chainchomplib.adapterlayer.Message import Message
from chainchomplib.data import SocketEvents
from socketio import AsyncClient

from chainchomp_service_layer.SocketEmitter import SocketEmitter


class MessageSendWorker(Thread):

    def __init__(self, queue: PriorityQueue, sio: AsyncClient):
        super().__init__()
        self.queue = queue
        self.is_running = True
        self.socket_emitter = SocketEmitter(sio)

    def run(self) -> None:
        while self.is_running:
            try:
                message: Message = self.queue.get(timeout=3)
            except Empty:
                LoggerInterface.warning('No messages to send to adapters')
                continue
            else:
                self.socket_emitter.emit_to_chainchomp_core(message.get_serialized())
