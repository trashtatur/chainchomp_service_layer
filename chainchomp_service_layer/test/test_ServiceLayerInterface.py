import unittest
from unittest.mock import MagicMock

from parameterized import parameterized

from chainchomp_service_layer import ConnectionThread, ServiceLayerInterface
from chainchomp_service_layer.resolver.ChainfileNameResolver import ChainfileNameResolver


class ServiceLayerInterfaceTest(unittest.TestCase):

    @parameterized.expand([
        ['testus', None],
        [None, 'testus']
    ])
    def test_that_it_should_correctly_handle_a_supplied_name(self, provided, found):
        name_resolver = self.get_chainfile_name_resolver_mock(found)
        thread = self.get_connection_thread_mock()
        uut = self.get_unit_under_test(thread, name_resolver)
        if not found:
            name_resolver.resolve.assert_not_called()
        if found:
            uut.set_up(self.callback_mock, found)
            thread.set_up.assert_called_with(found, self.callback_mock)
        if provided:
            uut.set_up(self.callback_mock, provided)
            thread.set_up.assert_called_with(provided, self.callback_mock)

    def get_chainfile_name_resolver_mock(self, return_name: str):
        resolver_mock = ChainfileNameResolver()
        resolver_mock.resolve = MagicMock(return_value=return_name)
        return resolver_mock

    def get_connection_thread_mock(self):
        connection_thread_mock = ConnectionThread()
        connection_thread_mock.run = MagicMock(return_value=None)
        connection_thread_mock.set_up = MagicMock(return_value=None)
        return connection_thread_mock

    def get_unit_under_test(
            self,
            connection_thread: ConnectionThread,
            chainfile_name_resolver: ChainfileNameResolver
    ) -> ServiceLayerInterface:
        return ServiceLayerInterface(connection_thread, chainfile_name_resolver)

    def callback_mock(self):
        pass