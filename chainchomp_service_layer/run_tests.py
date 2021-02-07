import os
import unittest

os.environ['CHAINCHOMP_TEST'] = '1'
loader = unittest.TestLoader()
start_dir = os.path.join(os.getcwd(), 'test')
suite = loader.discover(start_dir)

runner = unittest.TextTestRunner()
runner.run(suite)

os.environ['CHAINCHOMP_TEST'] = '0'
