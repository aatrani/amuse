from amuse.rfi.core import legacy_function, LegacyFunctionSpecification, CodeInterface
from amuse.community.interface.gd import GravitationalDynamicsInterface, GravitationalDynamics
from amuse.units import nbody_system, units

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

    @legacy_function
    def get_alpha():
        """
        Get alpha.
        """
        function = LegacyFunctionSpecification()
        function.addParameter('alpha', dtype='float64', direction=function.OUT,
                              description="alpha regularization parameter")
        function.result_type = 'int32'
        function.result_doc = """
        0 - OK
            the parameter was retrieved
        -1 - ERROR
            could not retrieve parameter
        """
        return function

    @legacy_function
    def set_alpha():
        """
        Set alpha.
        """
        function = LegacyFunctionSpecification()
        function.addParameter('alpha', dtype='float64', direction=function.IN,
                              description="alpha regularization parameter")
        function.result_type = 'int32'
        function.result_doc = """
        0 - OK
            the parameter was set
        -1 - ERROR
            could not set parameter
        """
        return function

    @legacy_function
    def get_beta():
        """
        Get beta.
        """
        function = LegacyFunctionSpecification()
        function.addParameter('beta', dtype='float64', direction=function.OUT,
                              description="beta regularization parameter")
        function.result_type = 'int32'
        function.result_doc = """
        0 - OK
            the parameter was retrieved
        -1 - ERROR
            could not retrieve parameter
        """
        return function

    @legacy_function
    def set_beta():
        """
        Set beta.
        """
        function = LegacyFunctionSpecification()
        function.addParameter('beta', dtype='float64', direction=function.IN,
                              description="beta regularization parameter")
        function.result_type = 'int32'
        function.result_doc = """
        0 - OK
            the parameter was set
        -1 - ERROR
            could not set parameter
        """
        return function

    @legacy_function
    def get_gamma():
        """
        Get gamma.
        """
        function = LegacyFunctionSpecification()
        function.addParameter('gamma', dtype='float64', direction=function.OUT,
                              description="gamma regularization parameter")
        function.result_type = 'int32'
        function.result_doc = """
        0 - OK
            the parameter was retrieved
        -1 - ERROR
            could not retrieve parameter
        """
        return function

    @legacy_function
    def set_gamma():
        """
        Set gamma.
        """
        function = LegacyFunctionSpecification()
        function.addParameter('gamma', dtype='float64', direction=function.IN,
                              description="gamma regularization parameter")
        function.result_type = 'int32'
        function.result_doc = """
        0 - OK
            the parameter was set
        -1 - ERROR
            could not set parameter
        """
        return function

    @legacy_function
    def set_usePNs():
        """ set_usePNs([0,1]): use post-Newtonians if 1
          if set to 0, post-Newtonians are not used"""
        function = LegacyFunctionSpecification()
        function.addParameter('usePNs', dtype='i', direction=function.IN)
        function.result_type = 'i'
        return function

    @legacy_function
    def get_usePNs():
        """ get_usePNs(): use post-Newtonians if 1 """
        function = LegacyFunctionSpecification()
        function.addParameter('usePNs', dtype='i', direction=function.OUT)
        function.result_type = 'i'
        return function

    @legacy_function
    def set_useTides():
        """ set_useTides([0,1]): use tides if 1
          if set to 0, tides are not used"""
        function = LegacyFunctionSpecification()
        function.addParameter('useTides', dtype='i', direction=function.IN)
        function.result_type = 'i'
        return function

    @legacy_function
    def get_useTides():
        """ get_useTides(): use tides if 1 """
        function = LegacyFunctionSpecification()
        function.addParameter('useTides', dtype='i', direction=function.OUT)
        function.result_type = 'i'
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

        handler.add_method_parameter(
            "get_begin_time",
            "set_begin_time",
            "begin_time",
            "model time to start the simulation at",
            default_value = 0.0 | nbody_system.time
        )

        handler.add_method_parameter(
            "get_alpha",
            "set_alpha",
            "alpha",
            "alpha regularization parameter",
            default_value=1.0
        )

        handler.add_method_parameter(
            "get_beta",
            "set_beta",
            "beta",
            "beta regularization parameter",
            default_value=0.0
        )

        handler.add_method_parameter(
            "get_gamma",
            "set_gamma",
            "gamma",
            "gamma regularization parameter",
            default_value=0.0
        )

        handler.add_boolean_parameter(
            "get_usePNs",
            "set_usePNs",
            "usePNs",
            "Post-Newtonians flag. True means: PNs (1PN/2PN/2.5PN) are included. "
            "False means: no Post-Newtonians are included",
            False
        )

        handler.add_boolean_parameter(
            "get_useTides",
            "set_useTides",
            "useTides",
            "Tides flag. True means: tidal forces are included. "
            "False means: no tidal forces are included",
            False
        )
