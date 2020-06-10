from amuse.rfi.core import legacy_function, LegacyFunctionSpecification, CodeInterface
from amuse.community.interface.gd import GravitationalDynamicsInterface, GravitationalDynamics

class TsunamiInterface(CodeInterface,
                       GravitationalDynamicsInterface):
    
    include_headers = ['worker_code.h']
    
    def __init__(self, **keyword_arguments):
        CodeInterface.__init__(self, name_of_the_worker="tsunami_worker", **keyword_arguments)
        
    
class Tsunami(GravitationalDynamics):

    def __init__(self, **options):
        GravitationalDynamics.__init__(self,  TsunamiInterface(**options), **options)
    
    def define_errorcodes(self, handler):
        handler.add_errorcode(-2, 'Called function is not implemented.')