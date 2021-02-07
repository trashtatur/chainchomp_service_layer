import inspect
import os

from chainchomplib import LoggerInterface
from chainchomplib.configlayer.resolver.ChainfileResolver import ChainfileResolver

from chainchomp_service_layer.ConnectionThread import ConnectionThread


class ServiceLayerInterface:

    def __init__(self):
        self.__connection_thread: ConnectionThread or None = None

    def set_up(self, callback, name=None):
        """
        This function sets up the connection th Chainchomps Core. When it is done, you can start emitting messages
        :param callback: A function that is called when messages arrive at your application
        :param name: This parameter is your chainlinks name. It is optional as Chainchomp can determine
        that itself most of the time
        :return:
        """
        chainlink_name = name
        if name is not None:
            frame_info = inspect.stack()[1]
            filepath = frame_info.filename
            del frame_info
            caller_path = os.path.abspath(filepath)
            chainlink_name = self.__get_chainfile_name(os.path.dirname(caller_path))

        if chainlink_name is None:
            LoggerInterface.error('No chainlink was found at the callers path. Aborting.')
            return
        self.__connection_thread = ConnectionThread(name, callback)
        self.__connection_thread.start()

    def emit(self, data):
        return self.__connection_thread.emit(data)

    def __get_chainfile_name(self, path) -> str or None:
        if os.path.isfile(os.path.join(path, 'chainfile.yml')):
            chainfile = ChainfileResolver.resolve(os.path.join(path, 'chainfile.yml'))
            return chainfile.chainlink_name

        upper_path = os.path.dirname(path)
        if upper_path == path:
            return None
        self.__get_chainfile_name(upper_path)
