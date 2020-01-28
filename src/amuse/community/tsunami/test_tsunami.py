from amuse.test.amusetest import TestWithMPI

from .interface import TsunamiInterface
from .interface import Tsunami

class TsunamiInterfaceTests(TestWithMPI):
    
    def test1(self):
        instance = TsunamiInterface()
        result,error = instance.echo_int(12)
        self.assertEquals(error, 0)
        self.assertEquals(result, 12)
        instance.stop()
    
