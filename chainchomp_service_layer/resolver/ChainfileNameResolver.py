import os

from chainchomplib.configlayer.resolver.ChainfileResolver import ChainfileResolver


class ChainfileNameResolver:

    def resolve(self, path) -> str or None:
        if os.path.isfile(os.path.join(path, 'chainfile.yml')):
            chainfile = ChainfileResolver.resolve(os.path.join(path, 'chainfile.yml'))
            return chainfile.chainlink_name

        upper_path = os.path.dirname(path)
        if upper_path == path:
            return None
        self.resolve(upper_path)