from amuse.rfi.core import legacy_function, LegacyFunctionSpecification, CodeInterface
from amuse.community.interface.gd import GravitationalDynamicsInterface, GravitationalDynamics

class TsunamiInterface(CodeInterface,
                       GravitationalDynamicsInterface):
    
    include_headers = ['worker_code.h']
    
    def __init__(self, **keyword_arguments):
        CodeInterface.__init__(self, name_of_the_worker="tsunami_worker", **keyword_arguments)
    
    @legacy_function
    def echo_int():
        function = LegacyFunctionSpecification()  
        function.addParameter('int_in', dtype='int32', direction=function.IN)
        function.addParameter('int_out', dtype='int32', direction=function.OUT)
        function.result_type = 'int32'
        function.can_handle_array = True
        return function
        
    
class Tsunami(GravitationalDynamics):

    def __init__(self, **options):
        GravitationalDynamics.__init__(self,  TsunamiInterface(**options), **options)
    
