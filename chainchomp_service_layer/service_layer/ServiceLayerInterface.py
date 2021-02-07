import inspect
import os

from chainchomplib import LoggerInterface

from chainchomp_service_layer.service_layer.ConnectionThread import ConnectionThread
from chainchomp_service_layer.resolver.ChainfileNameResolver import ChainfileNameResolver


class ServiceLayerInterface:

    def __init__(
            self,
            connection_thread: ConnectionThread,
            chainfile_name_resolver: ChainfileNameResolver
    ):
        self.chainfile_name_resolver = chainfile_name_resolver
        self.__connection_thread = connection_thread

    def set_up(self, callback, name=None):
        """
        This function sets up the connection th Chainchomps Core. When it is done, you can start emitting messages
        :param callback: A function that is called when messages arrive at your application
        :param name: This parameter is your chainlinks name. It is optional as Chainchomp can determine
        that itself most of the time
        :return:
        """
        chainlink_name = name
        if name is None:
            frame_info = inspect.stack()[1]
            filepath = frame_info.filename
            del frame_info
            caller_path = os.path.abspath(filepath)
            chainlink_name = self.chainfile_name_resolver.resolve(os.path.dirname(caller_path))

        if chainlink_name is None:
            LoggerInterface.error('No chainlink was found at the callers path. Aborting.')
            return
        self.__connection_thread.set_up(chainlink_name, callback)
        self.__connection_thread.start()

    def emit(self, data):
        return self.__connection_thread.emit(data)

