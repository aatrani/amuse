from amuse.test import amusetest

from amuse.units import units
from amuse.units import constants
from amuse.units import nbody_system
import numpy
import time
import sys

from amuse.datamodel import Particles
from amuse.datamodel import Particle
from amuse.couple import encounters


#codes to use
from amuse.community.kepler.interface import Kepler
from amuse.community.smalln.interface import SmallN

def new_binary(
        mass1, mass2, semi_major_axis,
        eccentricity = 0, keyoffset = 1,
        is_at_periapsis = True,
        G =  nbody_system.G 
    ):
    total_mass = mass1 + mass2
    mass_fraction_particle_1 = mass1 / (total_mass)

    binary = Particles(keys=range(keyoffset, keyoffset+2))
    binary[0].mass = mass1
    binary[1].mass = mass2

    mu = G * total_mass

    if is_at_periapsis:
        velocity = numpy.sqrt( mu / semi_major_axis  * ((1.0 + eccentricity)/(1.0 - eccentricity)))
        radius   = semi_major_axis * (1.0 - eccentricity)
    else:
        velocity = numpy.sqrt( mu / semi_major_axis  * ((1.0 - eccentricity)/(1.0 + eccentricity)))
        radius   = semi_major_axis * (1.0 + eccentricity)
        
    binary[0].position = ((1.0 - mass_fraction_particle_1) * radius * [1.0,0.0,0.0])
    binary[1].position = -(mass_fraction_particle_1 * radius * [1.0,0.0,0.0])

    binary[0].velocity = ((1.0 - mass_fraction_particle_1) * velocity * [0.0,1.0,0.0])
    binary[1].velocity = -(mass_fraction_particle_1 * velocity * [0.0,1.0,0.0])   

    return binary
        
class TestAbstractHandleEncounter(amusetest.TestWithMPI):
    
    def new_kepler(self):
        x = Kepler()
        x.initialize_code()
        return x
        
    def test1(self):
        particles_in_encounter = Particles(2)
        particles_in_encounter.mass = 1 | nbody_system.mass
        particles_in_encounter[0].position = [1,0,0] | nbody_system.length
        particles_in_encounter[1].position = [0,0,0] | nbody_system.length
        particles_in_encounter.velocity = [0,0.5,0] | nbody_system.speed
        
        particles_in_field = Particles(5)
        particles_in_field.mass = [1,2,3,4,5] | nbody_system.mass
        particles_in_field[0].position = [2,0,0] | nbody_system.length
        particles_in_field[1].position = [1.5,0,0] | nbody_system.length
        particles_in_field[2].position = [0.5,1,0] | nbody_system.length
        particles_in_field[3].position = [0.5,-0.5,0] | nbody_system.length
        particles_in_field[4].position = [0,0,2] | nbody_system.length
        particles_in_field.velocity = [0,0.0,0] | nbody_system.speed
        
        x = encounters.AbstractHandleEncounter(
            G = nbody_system.G,
            kepler_code = self.new_kepler()
        )
        
        x.particles_in_encounter.add_particles(particles_in_encounter)
        x.particles_in_field.add_particles(particles_in_field)
        
        x.execute()
        
        self.assertAlmostRelativeEqual(x.large_scale_of_particles_in_the_encounter, 1.0 | nbody_system.length)
        self.assertAlmostRelativeEqual(x.small_scale_of_particles_in_the_encounter, 1.0 | nbody_system.length)
        
        self.assertEquals(len(x.particles_close_to_encounter), 3)
        self.assertAlmostRelativeEqual(x.particles_close_to_encounter.mass, [2,3,4] | nbody_system.mass)
        
    def test2(self):
        
        particles_in_encounter = Particles(keys=(1,2))
        particles_in_encounter.mass = 1 | nbody_system.mass
        particles_in_encounter[0].position = [1,0,0] | nbody_system.length
        particles_in_encounter[1].position = [0,0,0] | nbody_system.length
        particles_in_encounter.velocity = [0,0.5,0] | nbody_system.speed
        
        particles_in_field = Particles(keys=(3,))
        particles_in_field.mass = 1 | nbody_system.mass
        particles_in_field[0].position = [3,0,0] | nbody_system.length
        
        particles_in_multiples = Particles()
        particles_in_multiples.add_particle(particles_in_encounter[0])
        multiple = particles_in_multiples[0]
        multiple.components = Particles(2)
        multiple.components.mass = 0.5 | nbody_system.mass
        multiple.components[0].position = [0,0.1,0] | nbody_system.length
        multiple.components[1].position = [0,-0.1,0] | nbody_system.length
        multiple.components[0].velocity = [0,0,0.2] | nbody_system.speed
        multiple.components[1].velocity = [0,0.1,-0.2] | nbody_system.speed
        multiple.components.child1 = None
        multiple.components.child2 = None
        
        x = encounters.AbstractHandleEncounter(
            G = nbody_system.G,
            kepler_code = self.new_kepler()
        )
        
        x.particles_in_encounter.add_particles(particles_in_encounter)
        x.particles_in_field.add_particles(particles_in_field)
        x.existing_multiples.add_particles(particles_in_multiples)
        
        x.execute()
        
        self.assertEquals(len(x.all_singles_in_encounter), 3)
        
        self.assertAlmostRelativeEqual(x.all_singles_in_encounter.mass, [0.5, 0.5, 1.0]| nbody_system.mass)
        
        child1 = x.singles_and_multiples_after_evolve[0]
        child2 = x.singles_and_multiples_after_evolve[1]
        self.assertAlmostRelativeEqual(child1.position, [1,0.1,0]| nbody_system.length)
        self.assertAlmostRelativeEqual(child1.velocity, [0,0.5,0.2]| nbody_system.speed)
        self.assertAlmostRelativeEqual(child2.position, [1,-0.1,0]| nbody_system.length)
        self.assertAlmostRelativeEqual(child2.velocity, [0,0.6,-0.2]| nbody_system.speed)
        
        
    def test3(self):
        
        particles_in_encounter = Particles(keys=(1,2))
        particles_in_encounter.mass = 1 | nbody_system.mass
        particles_in_encounter[0].position = [1,0,0] | nbody_system.length
        particles_in_encounter[1].position = [0,0,0] | nbody_system.length
        particles_in_encounter.velocity = [0,0.0,0] | nbody_system.speed
        
        particles_in_field = Particles(keys=(2,4,5,6,7,))
        particles_in_field.mass = [1,2,3,4,5] | nbody_system.mass
        particles_in_field[0].position = [2,0,0] | nbody_system.length
        particles_in_field[1].position = [1.5,0,0] | nbody_system.length
        particles_in_field[2].position = [0.5,1,0] | nbody_system.length
        particles_in_field[3].position = [0.5,-0.5,0] | nbody_system.length
        particles_in_field[4].position = [0,0,2] | nbody_system.length
        particles_in_field.velocity = [0,0,0]  | nbody_system.speed
        
        x = encounters.AbstractHandleEncounter(
            G = nbody_system.G,
            kepler_code = self.new_kepler()
        )
        
        x.particles_in_encounter.add_particles(particles_in_encounter)
        x.particles_in_field.add_particles(particles_in_field)
    
    
        simple_binary = new_binary(
            1 | nbody_system.mass, 
            1 | nbody_system.mass, 
            0.2 | nbody_system.length
        )
                
        def evolve_singles_in_encounter_until_end_state():
            particles = x.singles_and_multiples_after_evolve
            particles.add_particles(x.all_singles_in_encounter)
            particles.child1 = None
            particles.child2 = None
            
            root_particle = particles.add_particle(Particle(
                key = 10,
                mass = 2.0 | nbody_system.mass, 
                position = particles[0:2].center_of_mass(),
                velocity = particles[0:2].center_of_mass_velocity(),
            ))
            root_particle.child1 = particles[0]
            root_particle.child2 = particles[1]
            particles[0].position = simple_binary[0].position + root_particle.position
            particles[1].position = simple_binary[1].position + root_particle.position
            
            particles[0].velocity = simple_binary[0].velocity + root_particle.velocity
            particles[1].velocity = simple_binary[1].velocity + root_particle.velocity
        
        x.evolve_singles_in_encounter_until_end_state = evolve_singles_in_encounter_until_end_state
        x.determine_structure_of_the_evolved_state = lambda : 1
        
        x.execute()
        self.assertEquals(len(x.new_multiples), 1)
        self.assertEquals(len(x.new_binaries), 1)
        multiple = x.new_multiples[0]
        self.assertEquals(len(multiple.components), 2)
        
        self.assertAlmostRelativeEqual(multiple.components[0].position, simple_binary[0].position)
        self.assertAlmostRelativeEqual(multiple.components[1].position, simple_binary[1].position) 
    
    
        
    def test4(self):
        
        particles_in_encounter = Particles(keys=(1,2))
        particles_in_encounter.mass = 1 | nbody_system.mass
        particles_in_encounter[0].position = [1,0,0] | nbody_system.length
        particles_in_encounter[1].position = [0,0,0] | nbody_system.length
        particles_in_encounter.velocity = [0,0.0,0] | nbody_system.speed
        
        particles_in_field = Particles(keys=(3,4,5,6,7,))
        particles_in_field.mass = [1,2,3,4,5] | nbody_system.mass
        particles_in_field[0].position = [2,0,0] | nbody_system.length
        particles_in_field[1].position = [1.5,0,0] | nbody_system.length
        particles_in_field[2].position = [0.5,1,0] | nbody_system.length
        particles_in_field[3].position = [0.5,-0.5,0] | nbody_system.length
        particles_in_field[4].position = [0,0,2] | nbody_system.length
        particles_in_field.velocity = [0,0,0]  | nbody_system.speed
        
        binaries = Particles(keys=(20,))
        binaries[0].child1 = particles_in_encounter[0]
        binaries[0].child2 = particles_in_encounter[1]
        
        x = encounters.AbstractHandleEncounter(
            G = nbody_system.G,
            kepler_code = self.new_kepler()
        )
        
        x.particles_in_encounter.add_particles(particles_in_encounter)
        x.particles_in_field.add_particles(particles_in_field)
        x.existing_binaries.add_particles(binaries)
        
        
        simple_binary = new_binary(
            1 | nbody_system.mass, 
            1 | nbody_system.mass, 
            0.2 | nbody_system.length
        )
                
        def evolve_singles_in_encounter_until_end_state():
            particles = x.singles_and_multiples_after_evolve
            particles.add_particles(x.all_singles_in_encounter)
            particles.child1 = None
            particles.child2 = None
            
            root_particle = particles.add_particle(Particle(
                key = 10,
                mass = 2.0 | nbody_system.mass, 
                position = particles[0:2].center_of_mass(),
                velocity = particles[0:2].center_of_mass_velocity(),
            ))
            root_particle.child1 = particles[0]
            root_particle.child2 = particles[1]
            particles[0].position = simple_binary[0].position + root_particle.position
            particles[1].position = simple_binary[1].position + root_particle.position
            
            particles[0].velocity = simple_binary[0].velocity + root_particle.velocity
            particles[1].velocity = simple_binary[1].velocity + root_particle.velocity
        
        x.evolve_singles_in_encounter_until_end_state = evolve_singles_in_encounter_until_end_state
        x.determine_structure_of_the_evolved_state = lambda : 1
        
        x.execute()
        self.assertEquals(len(x.new_multiples), 1)
        self.assertEquals(len(x.new_binaries), 0)
        self.assertEquals(len(x.updated_binaries), 1)
        self.assertEquals(x.updated_binaries[0], binaries[0])



    def test5(self):
        
        particles_in_encounter = Particles(keys=(1,2))
        particles_in_encounter.mass = 1 | nbody_system.mass
        particles_in_encounter[0].position = [1,0,0] | nbody_system.length
        particles_in_encounter[1].position = [0,0,0] | nbody_system.length
        particles_in_encounter.velocity = [0,0.0,0] | nbody_system.speed
        
        particles_in_field = Particles(keys=(2,4,5,6,7,))
        particles_in_field.mass = [1,2,3,4,5] | nbody_system.mass
        particles_in_field[0].position = [2,0,0] | nbody_system.length
        particles_in_field[1].position = [1.5,0,0] | nbody_system.length
        particles_in_field[2].position = [0.5,1,0] | nbody_system.length
        particles_in_field[3].position = [0.5,-0.5,0] | nbody_system.length
        particles_in_field[4].position = [0,0,2] | nbody_system.length
        particles_in_field.velocity = [0,0,0]  | nbody_system.speed
        
        x = encounters.AbstractHandleEncounter(
            G = nbody_system.G,
            kepler_code = self.new_kepler()
        )
        
        x.particles_in_encounter.add_particles(particles_in_encounter)
        x.particles_in_field.add_particles(particles_in_field)
        
        
        simple_binary = new_binary(
            1 | nbody_system.mass, 
            1 | nbody_system.mass, 
            2 | nbody_system.length
        )
                
        def evolve_singles_in_encounter_until_end_state():
            particles = x.singles_and_multiples_after_evolve
            particles.add_particles(x.all_singles_in_encounter)
            particles.child1 = None
            particles.child2 = None
            
            root_particle = particles.add_particle(Particle(
                key = 10,
                mass = 2.0 | nbody_system.mass, 
                position = particles[0:2].center_of_mass(),
                velocity = particles[0:2].center_of_mass_velocity(),
            ))
            root_particle.child1 = particles[0]
            root_particle.child2 = particles[1]
            particles[0].position = simple_binary[0].position + root_particle.position
            particles[1].position = simple_binary[1].position + root_particle.position
            
            particles[0].velocity = simple_binary[0].velocity + root_particle.velocity
            particles[1].velocity = simple_binary[1].velocity + root_particle.velocity
        
        x.evolve_singles_in_encounter_until_end_state = evolve_singles_in_encounter_until_end_state
        x.determine_structure_of_the_evolved_state = lambda : 1
        
        x.execute()
        
        # no multiples as the binary is larger than the 
        # hard binary scale
        self.assertEquals(len(x.new_multiples), 0)
        self.assertEquals(len(x.new_binaries), 0)
        

    def test6(self):
        
        particles_in_encounter = Particles(keys=(1,2,3))
        particles_in_encounter.mass = 1 | nbody_system.mass
        particles_in_encounter[0].position = [1,0,0] | nbody_system.length
        particles_in_encounter[1].position = [0,0,0] | nbody_system.length
        particles_in_encounter[2].position = [0,0.5,0] | nbody_system.length
        particles_in_encounter.velocity = [0,0.0,0] | nbody_system.speed
        
        
        x = encounters.AbstractHandleEncounter(
            G = nbody_system.G,
            kepler_code = self.new_kepler()
        )
        x.particles_in_encounter.add_particles(particles_in_encounter)
        
        
        simple_binary_1 = new_binary(
            1 | nbody_system.mass, 
            1 | nbody_system.mass, 
            0.4 | nbody_system.length
        )
        simple_binary_top = new_binary(
            2 | nbody_system.mass, 
            1 | nbody_system.mass, 
            2 | nbody_system.length
        )
                
        def evolve_singles_in_encounter_until_end_state():
            particles = x.singles_and_multiples_after_evolve
            particles.add_particles(x.all_singles_in_encounter)
            particles.child1 = None
            particles.child2 = None
            
            inner_binary_particle = particles.add_particle(Particle(
                key = 10,
                mass = 2.0 | nbody_system.mass, 
                position = particles[0:2].center_of_mass(),
                velocity = particles[0:2].center_of_mass_velocity(),
            ))
            inner_binary_particle.child1 = particles[0]
            inner_binary_particle.child2 = particles[1]
            particles[0].position = simple_binary_1[0].position + inner_binary_particle.position
            particles[1].position = simple_binary_1[1].position + inner_binary_particle.position
            
            particles[0].velocity = simple_binary_1[0].velocity + inner_binary_particle.velocity
            particles[1].velocity = simple_binary_1[1].velocity + inner_binary_particle.velocity
            
            root_particle = particles.add_particle(Particle(
                key = 11,
                mass = 3.0 | nbody_system.mass, 
                position = particles.center_of_mass(),
                velocity = particles.center_of_mass_velocity(),
            ))
            
            root_particle.child1 = inner_binary_particle
            root_particle.child2 = particles[2]
            inner_binary_particle.position = simple_binary_top[0].position + root_particle.position
            particles[2].position = simple_binary_top[1].position + root_particle.position
            
            inner_binary_particle.velocity = simple_binary_top[0].velocity + root_particle.velocity
            particles[2].velocity = simple_binary_top[1].velocity + root_particle.velocity
            
            
            
        
        x.evolve_singles_in_encounter_until_end_state = evolve_singles_in_encounter_until_end_state
        x.determine_structure_of_the_evolved_state = lambda : 1
        
        x.execute()
        
        # no multiples as the binary is larger than the 
        # hard binary scale
        self.assertEquals(len(x.new_multiples), 1)
        self.assertEquals(len(x.new_binaries), 1)
        multiple = x.new_multiples[0]
        self.assertEquals(len(multiple.components), 2)
        self.assertAlmostRelativeEqual(multiple.components[0].key, particles_in_encounter[0].key)
        self.assertAlmostRelativeEqual(multiple.components[1].key, particles_in_encounter[1].key)
    
    
    
    def test7(self):
        
        particles_in_encounter = Particles(keys=(1,2,3))
        particles_in_encounter.mass = 1 | nbody_system.mass
        particles_in_encounter[0].position = [1,0,0] | nbody_system.length
        particles_in_encounter[1].position = [0,0,0] | nbody_system.length
        particles_in_encounter[2].position = [0,0.5,0] | nbody_system.length
        particles_in_encounter.velocity = [0,0.0,0] | nbody_system.speed
        
        
        x = encounters.AbstractHandleEncounter(
            G = nbody_system.G,
            kepler_code = self.new_kepler()
        )
        x.particles_in_encounter.add_particles(particles_in_encounter)
        
        multiples = Particles()
        particle_in_multiples = multiples.add_particle( particles_in_encounter[2])
        particle_in_multiples.components = Particles(keys=(4,5))
        particle_in_multiples.components.mass = 1 | nbody_system.mass
        particle_in_multiples.components[0].position = [0,0,0.2] | nbody_system.length
        particle_in_multiples.components[1].position = [0,0,-0.2] | nbody_system.length
        particle_in_multiples.components.velocity = [0,0.0,0] | nbody_system.speed
        particle_in_multiples.components.child1 = None
        particle_in_multiples.components.child2 = None
        x.existing_multiples.add_particles(multiples) 
        
                
        def evolve_singles_in_encounter_until_end_state():
            
            particles = x.singles_and_multiples_after_evolve
            particles.add_particles(x.all_singles_in_encounter)
            print particles
            particles.child1 = None
            particles.child2 = None
        
            
            
        
        x.evolve_singles_in_encounter_until_end_state = evolve_singles_in_encounter_until_end_state
        x.determine_structure_of_the_evolved_state = lambda : 1
        
        x.execute()
        
        # no multiples as the binary is larger than the 
        # hard binary scale
        self.assertEquals(len(x.new_multiples), 0)
        self.assertEquals(len(x.new_binaries), 0)
        self.assertEquals(len(x.dissolved_multiples), 1)
        self.assertEquals(len(x.released_singles), 2)
        self.assertTrue(particle_in_multiples.components[0] in x.released_singles)
        self.assertTrue(particle_in_multiples.components[1] in x.released_singles)

class TestKeplerOrbits(amusetest.TestWithMPI):
    
    def new_kepler(self):
        x = Kepler()
        x.initialize_code()
        return x
        
    def test1(self):
        x = encounters.KeplerOrbits(self.new_kepler())
        binary = new_binary( 
            1 | nbody_system.mass,
            0.5 | nbody_system.mass,
            1.2 | nbody_system.length,
        )
        semimajor_axis, eccentricity = x.get_semimajor_axis_and_eccentricity_for_binary_components(
            binary[0],
            binary[1]
        )
        self.assertAlmostRelativeEquals(semimajor_axis,  1.2 | nbody_system.length)
        self.assertAlmostRelativeEquals(eccentricity,  0)
        
    def test2(self):
        x = encounters.KeplerOrbits(self.new_kepler())
        binary = new_binary( 
            1 | nbody_system.mass,
            0.5 | nbody_system.mass,
            2.0 | nbody_system.length,
            0.5,
            is_at_periapsis = False
            
        )
        binary.position += [0.1,0.2,0.3]  | nbody_system.length
        binary.velocity += [0.4,0.5,0.6]  | nbody_system.speed
        
        dpos, dvel = x.compress_binary(
            binary,
            1.2 | nbody_system.length
        )
        
        center_of_mass_before = binary.center_of_mass()
        center_of_mass_velocity_before = binary.center_of_mass_velocity()
        
        binary.position += dpos
        binary.velocity += dvel
        
        center_of_mass_after = binary.center_of_mass()
        center_of_mass_velocity_after = binary.center_of_mass_velocity()
        
        self.assertAlmostRelativeEquals(center_of_mass_before, center_of_mass_after)
        self.assertAlmostRelativeEquals(center_of_mass_velocity_before, center_of_mass_velocity_after)
        separation = (binary[0].position  - binary[1].position).length()
        self.assertAlmostRelativeEquals( separation, 1.2 | nbody_system.length)
    
    def test3(self):
        x = encounters.KeplerOrbits(self.new_kepler())
        binary = new_binary( 
            1 | nbody_system.mass,
            0.5 | nbody_system.mass,
            2.0 | nbody_system.length,
            0.5,
            is_at_periapsis = True
            
        )
        binary.position += [0.1,0.2,0.3]  | nbody_system.length
        binary.velocity += [0.4,0.5,0.6]  | nbody_system.speed
        
        dpos, dvel = x.expand_binary(
            binary,
            2.5 | nbody_system.length
        )
        
        center_of_mass_before = binary.center_of_mass()
        center_of_mass_velocity_before = binary.center_of_mass_velocity()
        
        binary.position += dpos
        binary.velocity += dvel
        
        center_of_mass_after = binary.center_of_mass()
        center_of_mass_velocity_after = binary.center_of_mass_velocity()
        
        self.assertAlmostRelativeEquals(center_of_mass_before, center_of_mass_after, 8)
        self.assertAlmostRelativeEquals(center_of_mass_velocity_before, center_of_mass_velocity_after, 8)
        separation = (binary[0].position  - binary[1].position).length()
        self.assertAlmostRelativeEquals( separation, 2.5 | nbody_system.length)
    
    
    def test4(self):
        converter = nbody_system.nbody_to_si(1 | units.MSun, 1 | units.AU)
        kepler = Kepler(converter)
        kepler.initialize_code()
        x = encounters.KeplerOrbits(kepler)
        binary = new_binary( 
            1 | units.MSun,
            0.5 | units.MSun,
            1.2 | units.AU,
            G = constants.G
        )
        semimajor_axis, eccentricity = x.get_semimajor_axis_and_eccentricity_for_binary_components(
            binary[0],
            binary[1]
        )
        self.assertAlmostRelativeEquals(semimajor_axis,  1.2 | units.AU, 8)
        self.assertAlmostRelativeEquals(eccentricity,  0)

class TestScaleSystem(amusetest.TestWithMPI):
    
    def new_kepler(self):
        x = Kepler()
        x.initialize_code()
        return x
        
    def test1(self):
        kepler = encounters.KeplerOrbits(self.new_kepler())
        binary = new_binary( 
            1 | nbody_system.mass,
            0.5 | nbody_system.mass,
            1.2 | nbody_system.length,
            0.5,
            is_at_periapsis = False
        )
        binary.radius = 0 |  nbody_system.length
        
        x = encounters.ScaleSystem(kepler)
        self.assertTrue((binary[0].position - binary[1].position).length() > 1.5 | nbody_system.length)
        x.scale_particles_to_sphere(binary, 0.75 | nbody_system.length)
        self.assertTrue((binary[0].position - binary[1].position).length() <= 1.6 | nbody_system.length)
        print (binary[0].position - binary[1].position).length()
        self.assertTrue((binary[0].position - binary[1].position).length() >= (1.5 - 1e-6)| nbody_system.length )
        
    
    
    def test2(self):
        kepler = encounters.KeplerOrbits(self.new_kepler())
        binary = new_binary( 
            1 | nbody_system.mass,
            0.5 | nbody_system.mass,
            1.2 | nbody_system.length,
            0.5,
            is_at_periapsis = True
        )
        binary.radius = 0 |  nbody_system.length
        
        x = encounters.ScaleSystem(kepler)
        self.assertTrue((binary[0].position - binary[1].position).length() < 1.5 | nbody_system.length)
        x.scale_particles_to_sphere(binary, 0.75 | nbody_system.length)
        self.assertTrue((binary[0].position - binary[1].position).length() <= 1.6 | nbody_system.length)
        print (binary[0].position - binary[1].position).length()
        self.assertTrue((binary[0].position - binary[1].position).length() >= (1.5 - 1e-6)| nbody_system.length )
        
      
    def test3(self):
        kepler = encounters.KeplerOrbits(self.new_kepler())
        
        particles= Particles(keys=(1,2))
        particles.mass = 1 | nbody_system.mass
        particles[0].position = [1,0,0] | nbody_system.length
        particles[0].velocity = [1,0.0,0] | nbody_system.speed
        
        particles[1].position = [-1,0,0] | nbody_system.length
        particles[1].velocity = [-1,0.0,0] | nbody_system.speed
        
        particles.radius = 0 |  nbody_system.length
        
        x = encounters.ScaleSystem(kepler)
        
        print (particles[0].position - particles[1].position).length() 
        self.assertTrue((particles[0].position - particles[1].position).length() > 1.5 | nbody_system.length)
        
        x.scale_particles_to_sphere(particles, 0.75 | nbody_system.length)
        
        self.assertTrue((particles[0].position - particles[1].position).length() <= 1.6 | nbody_system.length)
        print particles
        self.assertTrue((particles[0].position - particles[1].position).length() >= (1.5 - 1e-6)| nbody_system.length )
        self.assertAlmostRelativeEquals(particles[0].position,  [0.75,0,0] | nbody_system.length)
        self.assertAlmostRelativeEquals(particles[1].position,  [-0.75,0,0] | nbody_system.length)
        
        
    def test4(self):
        kepler = encounters.KeplerOrbits(self.new_kepler())
        
        particles= Particles(keys=(1,2,3,4,5,6))
        particles.mass = 1 | nbody_system.mass
        for i in range(3):
            position = [0,0,0] | nbody_system.length
            position[i] = 1 | nbody_system.length
            particles[i].position =  position
            position[i] = -1 | nbody_system.length
            particles[i+3].position =  position
            
            velocity = [0,0,0] | nbody_system.speed
            velocity[i] = 1 | nbody_system.speed
            particles[i].velocity =  velocity
            velocity[i] = -1 | nbody_system.speed
            particles[i+3].velocity =  velocity

        particles.radius = 0 |  nbody_system.length
        
        
        x = encounters.ScaleSystem(kepler)
        
        potential_energy0 = particles.potential_energy(G = nbody_system.G)
        kinetic_energy0 = particles.kinetic_energy()
        
        x.scale_particles_to_sphere(particles, 0.5 | nbody_system.length)
        
        
        self.assertAlmostRelativeEquals(particles[0].position,  [1/numpy.sqrt(2),0,0] | nbody_system.length)
        self.assertAlmostRelativeEquals(particles[3].position,  [-1/numpy.sqrt(2),0,0] | nbody_system.length)
        self.assertAlmostRelativeEquals(particles[0].velocity,  [1.542,0,0] | nbody_system.speed, 3)
        self.assertAlmostRelativeEquals(particles[3].velocity,  [-1.542,0,0] | nbody_system.speed, 3)
        
        potential_energy1 = particles.potential_energy(G = nbody_system.G)
        kinetic_energy1 = particles.kinetic_energy()
        
        
        self.assertAlmostRelativeEquals(potential_energy0 + kinetic_energy0,potential_energy1 + kinetic_energy1)


class TestHandleEncounter(amusetest.TestWithMPI):
    
    def new_kepler(self):
        x = Kepler()
        x.initialize_code()
        return x
        
    def test1(self):
        particles_in_encounter = Particles(keys=(1,2,3))
        particles_in_encounter.mass = 1 | nbody_system.mass
        particles_in_encounter[0].position = [1,0,0] | nbody_system.length
        particles_in_encounter[1].position = [0,0,0] | nbody_system.length
        particles_in_encounter[2].position = [0,0.5,0] | nbody_system.length
        particles_in_encounter.velocity = [0,0.0,0] | nbody_system.speed
        
        particles_in_field = Particles()
        
        x = encounters.HandleEncounter(
            kepler_code = self.new_kepler(),
            resolve_collision_code = SmallN(),
            interaction_over_code = None,
            G = nbody_system.G
        )
        
        x.particles_in_encounter.add_particles(particles_in_encounter)
        
        x.execute()
        self.assertEquals(len(x.new_multiples), 1)
        self.assertEquals(len(x.new_binaries), 1)
        multiple = x.new_multiples[0]
        self.assertEquals(len(multiple.components), 2)
        self.assertAlmostRelativeEqual(multiple.components[0].key, particles_in_encounter[0].key)
        self.assertAlmostRelativeEqual(multiple.components[1].key, particles_in_encounter[1].key)
        self.assertEquals(len(x.captured_singles), 2)
        self.assertEquals(x.captured_singles.key, [1,2])
    

    def test2(self):
        particles_in_encounter = Particles(keys=(1,2))
        particles_in_encounter.mass = 2 | nbody_system.mass
        particles_in_encounter[0].position = [1,0,0] | nbody_system.length
        particles_in_encounter[1].position = [0,0,0] | nbody_system.length
        particles_in_encounter.velocity = [0,0.0,0] | nbody_system.speed
        
        
        binary1 = new_binary(
            1 | nbody_system.mass, 
            1 | nbody_system.mass, 
            0.01 | nbody_system.length,
            keyoffset = 30
        )
        binary2 = new_binary(
            1 | nbody_system.mass, 
            1 | nbody_system.mass, 
            0.01 | nbody_system.length,
            keyoffset = 40
        )
        binaries = Particles(keys=(20,21))
        binaries[0].child1 = binary1[0]
        binaries[0].child2 = binary1[1]
        binaries[1].child1 = binary2[0]
        binaries[1].child2 = binary2[1]
        binary1.child1 = None
        binary1.child2 = None
        binary2.child1 = None
        binary2.child2 = None
        
        multiples = Particles()
        multiple = particles_in_encounter[0]
        multiple.components = binary1
        multiples.add_particle(multiple)
        multiple = particles_in_encounter[1]
        multiple.components = binary2
        multiples.add_particle(multiple)
        
        x = encounters.HandleEncounter(
            kepler_code = self.new_kepler(),
            resolve_collision_code = SmallN(),
            interaction_over_code = None,
            G = nbody_system.G
        )
        
        x.particles_in_encounter.add_particles(particles_in_encounter)
        x.existing_binaries.add_particles(binaries)
        x.existing_multiples.add_particles(multiples)
        
        
        x.execute()
        self.assertEquals(len(x.new_multiples), 2)
        self.assertEquals(len(x.new_binaries), 2)
        self.assertEquals(len(x.captured_singles), 0)
        self.assertEquals(len(x.released_singles), 0)
        
        multiple = x.new_multiples[0]
        self.assertEquals(len(multiple.components), 2)
    
    
        self.assertAlmostRelativeEqual(multiple.components[0].key, binaries[0].child1.key)
        self.assertAlmostRelativeEqual(multiple.components[1].key, binaries[1].child1.key)
        multiple = x.new_multiples[1]
        self.assertEquals(len(multiple.components), 2)
        self.assertAlmostRelativeEqual(multiple.components[0].key, binaries[0].child2.key)
        self.assertAlmostRelativeEqual(multiple.components[1].key, binaries[1].child2.key)

    def test3(self):
        particles_in_encounter = Particles(keys=(1,2))
        particles_in_encounter.mass = 2 | nbody_system.mass
        particles_in_encounter[0].position = [1,0,0] | nbody_system.length
        particles_in_encounter[1].position = [0,0,0] | nbody_system.length
        particles_in_encounter.velocity = [0,0.0,0] | nbody_system.speed
        
        
        binary1 = new_binary(
            1 | nbody_system.mass, 
            1 | nbody_system.mass, 
            0.01 | nbody_system.length,
            keyoffset = 30
        )
        binaries = Particles(keys=(20,))
        binaries[0].child1 = binary1[0]
        binaries[0].child2 = binary1[1]
        binary1.child1 = None
        binary1.child2 = None
        
        multiples = Particles()
        multiple = particles_in_encounter[0]
        multiple.components = binary1
        multiples.add_particle(multiple)
        
        x = encounters.HandleEncounter(
            kepler_code = self.new_kepler(),
            resolve_collision_code = SmallN(),
            interaction_over_code = None,
            G = nbody_system.G
        )
        
        x.particles_in_encounter.add_particles(particles_in_encounter)
        x.existing_binaries.add_particles(binaries)
        x.existing_multiples.add_particles(multiples)
        
        x.execute()
        
        self.assertEquals(len(x.new_multiples), 1)
        self.assertEquals(len(x.dissolved_multiples), 1)
        self.assertEquals(len(x.new_binaries), 1)
        self.assertEquals(len(x.captured_singles), 1)
        self.assertEquals(len(x.released_singles), 1)
        
        multiple = x.new_multiples[0]
        print multiple.child1
        self.assertEquals(len(multiple.components), 2)
        print multiple.components
        
    
