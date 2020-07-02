import os
import sys
import numpy as np
import math

from amuse.community.tsunami.interface import TsunamiInterface, Tsunami

from amuse.units import nbody_system
from amuse.datamodel import Particles
from amuse.units import units
from amuse import datamodel
from amuse.ic import plummer
from amuse.ic.plummer import new_plummer_model
import matplotlib.pyplot as plt

code = Tsunami(redirection="null")

pythagorean = Particles(3)
pythagorean.mass = [3., 4., 5.] | nbody_system.mass
pythagorean.position = [[1., 3., 0.], [-2., -1., 0.], [1., -1., 0.]] | nbody_system.length
pythagorean.velocity = [[0., 0., 0.], [0., 0., 0.], [0., 0., 0.]] | nbody_system.length / nbody_system.time
pythagorean.radius = [0., 0., 0.] | nbody_system.length

print(pythagorean)
code.particles.add_particles(pythagorean)
#print(code.parameters)
code.parameters.tolerance = 1e-12
#print(code.parameters)

code_to_pythagorean = code.particles.new_channel_to(pythagorean)

print(code.particles)

print(code.parameters)
code.parameters.tolerance = 1e-13
code.parameters.usePNs = False
code.parameters.begin_time = 5 | nbody_system.time

#code.parameters.alpha = 0.0
#code.parameters.beta = 0.0
#code.parameters.gamma = 1.0

print(code.parameters)
code.cleanup_code

totp = []
totp.append(pythagorean.position.value_in(nbody_system.length))

dt = 0.1 | nbody_system.time
ft = 70 | nbody_system.time
realt = 0 | nbody_system.time
onetime = True
while (realt < ft):
    realt = realt + dt

    code.evolve_model(realt)
    code_to_pythagorean.copy()

    print(code.get_time(), code.get_deltaE())

    totp.append(pythagorean.position.value_in(nbody_system.length))

totp = np.vstack(totp)

fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_aspect('equal')
ax.plot(totp[::3, 0], totp[::3, 1], lw=2.5)
ax.plot(totp[1::3, 0], totp[1::3, 1], lw=2.5)
ax.plot(totp[2::3, 0], totp[2::3, 1], lw=2.5)
plt.show()
