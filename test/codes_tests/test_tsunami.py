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


code = Tsunami(redirection="none")

particles = new_plummer_model(5)
code.particles.add_particles(particles)
print(particles)

code.particles.remove_particle(particles[0])
code.particles[2].velocity = (1,  1, 1) | nbody_system.length / nbody_system.time


code.particles[1].mass = 1 | nbody_system.mass

print(code.particles)

code.particles.remove_particles(particles[1:3])

print(code.particles[0].position)

print(code.particles)

otherparticles = new_plummer_model(2)
otherparticles2 = new_plummer_model(3)

code.particles.add_particles(otherparticles)
code.particles.add_particles(otherparticles2)

print(code.particles)

code.particles.remove_particle(otherparticles2[0])

print(code.particles)

code.evolve_model(1 | nbody_system.time)

code.evolve_model(1 | nbody_system.time)


print(code.particles)

code.particles[1].position = (1,  1, 1) | nbody_system.length

code.particles[2].velocity = (1,  1, 1) | nbody_system.length / nbody_system.time

code.particles.add_particle(otherparticles2[0])

code.evolve_model(1 | nbody_system.time)

print(code.particles.position[0])
print(code.particles)

code.stop()






