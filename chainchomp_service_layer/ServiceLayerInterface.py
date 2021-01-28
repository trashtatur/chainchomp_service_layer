from chainchomp_service_layer.ConnectionThread import ConnectionThread


class ServiceLayerInterface:

    def __init__(self):
        self.__connection_thread: ConnectionThread or None = None

    def set_up(self, name, callback):
        self.__connection_thread = ConnectionThread(name, callback)
        self.__connection_thread.start()

    def emit(self, data):
        return self.__connection_thread.emit(data)
