from amuse.rfi.core import legacy_function, LegacyFunctionSpecification, CodeInterface
from amuse.community.interface.gd import GravitationalDynamicsInterface, GravitationalDynamics
from amuse.units import nbody_system, units
from amuse.community import NO_UNIT

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
    def get_deltaE():
        """
        Get energy error.
        """
        function = LegacyFunctionSpecification()
        function.addParameter('deltaE', dtype='float64', direction=function.OUT,
                              description="Energy error")
        function.result_type = 'int32'
        function.result_doc = """
        0 - OK
            the parameter was retrieved
        -1 - ERROR
            could not retrieve parameter
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

    @legacy_function
    def get_timelag():
        """
        Retrieve the timelag of a particle.
        """
        function = LegacyFunctionSpecification()
        function.addParameter('index_of_the_particle',
                              dtype='int32',
                              direction=function.IN,
                              description = "Index of the particle to get the timelag of. This index must have been returned by an earlier call to :meth:`new_particle`")
        function.addParameter('timelag',
                              dtype='float64',
                              unit=nbody_system.time,
                              direction=function.OUT,
                              description = "The timelag of the particle")
        function.result_type = 'int32'
        function.can_handle_array = True

    @legacy_function
    def set_timelag():
        """
        Set the timelag of a particle
        """
        function = LegacyFunctionSpecification()
        function.addParameter('index_of_the_particle',
                              dtype='int32',
                              direction=function.IN,
                              description = "Index of the particle to get the timelag of. This index must have been returned by an earlier call to :meth:`new_particle`")
        function.addParameter('timelag',
                              dtype='float64',
                              direction=function.IN,
                              unit=nbody_system.time,
                              description = "The timelag of the particle")
        function.result_type = 'int32'
        function.can_handle_array = True
        function.result_doc = """
        0 - OK
            particle was found in the model and the information was retreived
        -1 - ERROR
            particle could not be found
        """
        return function

    @legacy_function
    def get_kaps():
        """
        Retrieve the timelag of a particle.
        """
        function = LegacyFunctionSpecification()
        function.addParameter('index_of_the_particle',
                              dtype='int32',
                              direction=function.IN,
                              description = "Index of the particle to get the kaps of. This index must have been returned by an earlier call to :meth:`new_particle`")
        function.addParameter('kaps',
                              dtype='float64',
                              unit=NO_UNIT,
                              direction=function.OUT,
                              description = "The apsidal constant of the particle")
        function.result_type = 'int32'
        function.can_handle_array = True

    @legacy_function
    def set_kaps():
        """
        Set the apsidal constant of a particle
        """
        function = LegacyFunctionSpecification()
        function.addParameter('index_of_the_particle', dtype='int32', direction=function.IN,
            description = "Index of the particle to get the apsidal constant of. This index must have been returned by an earlier call to :meth:`new_particle`")
        function.addParameter('kaps', dtype='float64', direction=function.IN, unit=NO_UNIT, description = "The apsidal constant of the particle")
        function.result_type = 'int32'
        function.can_handle_array = True
        function.result_doc = """
        0 - OK
            particle was found in the model and the information was retreived
        -1 - ERROR
            particle could not be found
        """
        return function

    @legacy_function
    def get_adiabatic_index():
        """
        Retrieve the adiabatic index constant of a particle.
        """
        function = LegacyFunctionSpecification()
        function.addParameter('index_of_the_particle',
                              dtype='int32',
                              direction=function.IN,
                              description = "Index of the particle to get the adiabatic index of. This index must have been returned by an earlier call to :meth:`new_particle`")
        function.addParameter('adiabatic_index',
                              dtype='float64',
                              unit=NO_UNIT,
                              direction=function.OUT,
                              description = "The adiabatic index of the particle")
        function.result_type = 'int32'
        function.can_handle_array = True

    @legacy_function
    def set_adiabatic_index():
        """
        Set the adiabatic index of a particle
        """
        function = LegacyFunctionSpecification()
        function.addParameter('index_of_the_particle', dtype='int32', direction=function.IN,
            description = "Index of the particle to get the adiabatic index of. This index must have been returned by an earlier call to :meth:`new_particle`")
        function.addParameter('adiabatic_index', dtype='float64', direction=function.IN, unit=NO_UNIT, description = "The adiabatic index of the particle")
        function.result_type = 'int32'
        function.can_handle_array = True
        function.result_doc = """
        0 - OK
            particle was found in the model and the information was retreived
        -1 - ERROR
            particle could not be found
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

    def define_methods(self, handler):
        GravitationalDynamics.define_methods(self, handler)

        handler.add_method(
            "get_time",
            (),
            (nbody_system.time, handler.ERROR_CODE,)
        )

        handler.add_method(
            "get_deltaE",
            (),
            (handler.NO_UNIT, handler.ERROR_CODE,)
        )

        # handler.add_method(
        #     "set_timelag",
        #     (
        #         handler.NO_UNIT,
        #         nbody_system.time,
        #     ),
        #     (
        #         handler.ERROR_CODE
        #     )
        # )
        # handler.add_method(
        #     "get_timelag",
        #     (
        #         handler.NO_UNIT,
        #     ),
        #     (
        #         nbody_system.time,
        #         handler.ERROR_CODE
        #     )
        # )
        #
        # handler.add_method(
        #     "set_kaps",
        #     (
        #         handler.NO_UNIT,
        #         handler.NO_UNIT,
        #     ),
        #     (
        #         handler.ERROR_CODE
        #     )
        # )
        # handler.add_method(
        #     "get_kaps",
        #     (
        #         handler.NO_UNIT,
        #     ),
        #     (
        #         handler.NO_UNIT,
        #         handler.ERROR_CODE
        #     )
        # )
        #
        # handler.add_method(
        #     "set_adiabatic_index",
        #     (
        #         handler.NO_UNIT,
        #         handler.NO_UNIT,
        #     ),
        #     (
        #         handler.ERROR_CODE
        #     )
        # )
        # handler.add_method(
        #     "get_adiabatic_index",
        #     (
        #         handler.NO_UNIT,
        #     ),
        #     (
        #         handler.NO_UNIT,
        #         handler.ERROR_CODE
        #     )
        # )

    def define_particle_sets(self, handler):
        GravitationalDynamics.define_particle_sets(self, handler)

        handler.add_getter('particles', 'get_timelag', names = ('timelag',))
        handler.add_setter('particles', 'set_timelag', names = ('timelag',))
        handler.add_getter('particles', 'get_kaps', names=('kaps',))
        handler.add_setter('particles', 'set_kaps', names=('kaps',))
        handler.add_getter('particles', 'get_adiabatic_index', names=('adiabatic_index',))
        handler.add_setter('particles', 'set_adiabatic_index', names=('adiabatic_index',))

    def define_state(self, handler):
        GravitationalDynamics.define_state(self, handler)

        handler.add_method('RUN', 'get_timelag')
        handler.add_method('RUN', 'get_kaps')
        handler.add_method('RUN', 'get_adiabatic_index')

        handler.add_method('UPDATE', 'set_timelag')
        handler.add_method('UPDATE', 'set_kaps')
        handler.add_method('UPDATE', 'set_adiabatic_index')

        #handler.add_method('EDIT', 'set_state')
        #handler.add_method('EDIT', 'set_velocity')
        #handler.add_method('EDIT', 'set_mass')
        #handler.add_method('EDIT', 'set_position')
        #handler.add_method('CHANGED', 'before_get_parameter')

        #self.stopping_conditions.define_state(handler)