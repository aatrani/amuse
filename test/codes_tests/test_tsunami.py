import os
import sys
import numpy
import math

from amuse.community.tsunami.interface import TsunamiInterface, Tsunami

from amuse.units import nbody_system
from amuse.units import units
from amuse import datamodel
from amuse.ic import plummer
from amuse.ic.plummer import new_plummer_model


code = Tsunami()

particles = new_plummer_model(5)
code.particles.add_particles(particles)
print(particles)
print(code.particles)

code.particles.remove_particles(particles[2:4])

print(code.particles)

del code





