from queue import PriorityQueue, Empty
from threading import Thread

from chainchomplib import LoggerInterface
from chainchomplib.adapterlayer.Message import Message
from socketio import AsyncClient

from chainchomp_service_layer.service_layer.SocketEmitter import SocketEmitter


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
                self.socket_emitter.emit(message.get_serialized())
