from chainchomp_service_layer.service_layer.ConnectionThread import ConnectionThread
from chainchomp_service_layer.service_layer.ServiceLayerInterface import ServiceLayerInterface
from chainchomp_service_layer.resolver.ChainfileNameResolver import ChainfileNameResolver

interface = ServiceLayerInterface(ConnectionThread(), ChainfileNameResolver())
