from amuse.rfi.core import legacy_function, LegacyFunctionSpecification, CodeInterface
from amuse.community.interface.gd import GravitationalDynamicsInterface, GravitationalDynamics

class TsunamiInterface(CodeInterface,
                       GravitationalDynamicsInterface):
    
    include_headers = ['worker_code.h']
    
    def __init__(self, **keyword_arguments):
        CodeInterface.__init__(self, name_of_the_worker="tsunami_worker", **keyword_arguments)

    @legacy_function
    def get_tolerance():
        """
        Get tolerance.
        """
        function = LegacyFunctionSpecification()
        function.addParameter('tolerance', dtype='float64', direction=function.OUT,
                              description="BS extrapolator tolerance")
        function.result_type = 'int32'
        function.result_doc = """
        0 - OK
            the parameter was retrieved
        -1 - ERROR
            could not retrieve parameter
        """
        return function

    @legacy_function
    def set_tolerance():
        """
        Set tolerance.
        """
        function = LegacyFunctionSpecification()
        function.addParameter('tolerance', dtype='float64', direction=function.IN,
                              description="BS extrapolator tolerance")
        function.result_type = 'int32'
        function.result_doc = """
        0 - OK
            the parameter was set
        -1 - ERROR
            could not set parameter
        """
        return function

class Tsunami(GravitationalDynamics):

    def __init__(self, **options):
        GravitationalDynamics.__init__(self,  TsunamiInterface(**options), **options)
    
    def define_errorcodes(self, handler):
        handler.add_errorcode(-2, 'Called function is not implemented.')

    def define_parameters(self, handler):

        handler.add_method_parameter(
            "get_tolerance",
            "set_tolerance",
            "tolerance",
            "BS extrapolator tolerance",
            default_value= 1.0e-13
        )
