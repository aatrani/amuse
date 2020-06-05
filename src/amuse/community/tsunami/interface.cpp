#include "worker_code.h"
#include "tsunami4py.h"
#include <algorithm>
#include <cstring>
#include <cassert>

using std::cout;
using std::endl;

Tsunami *tsunami4py = nullptr;
bool initialized = false;
bool is_interface_uptodate = false;

size_t tmp_Npart = 0;

int tmp_new_particle_id = 0;
std::vector<int> tmp_idlist;

std::vector<ch_real> tmp_mass;
std::vector<ch_real> tmp_rad;
std::vector<ch_real3> tmp_pos;
std::vector<ch_real3> tmp_vel;

int sync_from_internals_to_interface() {
    if(initialized and not is_interface_uptodate) {
        //From code into std::vectors
        memcpy(&tmp_mass[0], &tsunami4py->mass[0], sizeof(ch_real)*tsunami4py->Npart);
        memcpy(&tmp_rad[0], &tsunami4py->rad[0], sizeof(ch_real)*tsunami4py->Npart);
        memcpy(&tmp_pos[0], &tsunami4py->pos[0], sizeof(ch_real3)*tsunami4py->Npart);
        memcpy(&tmp_vel[0], &tsunami4py->vel[0], sizeof(ch_real3)*tsunami4py->Npart);

        is_interface_uptodate = true;
    }
    return 0;
}

int sync_from_interface_to_internals() {
    assert(initialized);

    for(size_t i = 0; i < tmp_Npart; i++) {
        tsunami4py->pos[i].x = tmp_pos[i].x;
        tsunami4py->pos[i].y = tmp_pos[i].y;
        tsunami4py->pos[i].z = tmp_pos[i].z;
        tsunami4py->vel[i].x = tmp_vel[i].x;
        tsunami4py->vel[i].y = tmp_vel[i].y;
        tsunami4py->vel[i].z = tmp_vel[i].z;
        tsunami4py->mass[i] = tmp_mass[i];
        tsunami4py->soft[i] = 0.0; // Softening zero by default
        tsunami4py->rad[i] = tmp_rad[i];
        //TODO LATER tsunami4py->xdata[i].stype = static_cast<ptype>(stype_in[i]);
    }

    return 0;
}

int initialize_code() {
    tsunami4py = new Tsunami();
    return 0;
}

int cleanup_code() {
    delete tsunami4py;
    initialized = false;
    return 0;
}

int new_particle(int * index_of_the_particle, double mass, double x,
                 double y, double z, double vx, double vy, double vz, double radius){

    sync_from_internals_to_interface();

    tmp_Npart++;
    *index_of_the_particle = tmp_new_particle_id;

    tmp_idlist.push_back(tmp_new_particle_id);
    tmp_mass.push_back(mass);
    tmp_rad.push_back(radius);
    tmp_pos.emplace_back(x,y,z);
    tmp_vel.emplace_back(vx,vy,vz);

    tmp_new_particle_id++;

    // Needs re-initialization

    return 0;
}

int delete_particle(int index_of_the_particle){

    // Need to sync so when recomming particles, we can simply update
    sync_from_internals_to_interface();

    size_t ind = find(tmp_idlist.begin(), tmp_idlist.end(), index_of_the_particle) - tmp_idlist.begin();

    if (ind >= tmp_Npart) {
        return -1;
    }

    tmp_idlist.erase(tmp_idlist.begin() + ind);
    tmp_pos.erase(tmp_pos.begin() + ind);
    tmp_vel.erase(tmp_vel.begin() + ind);
    tmp_mass.erase(tmp_mass.begin() + ind);
    tmp_rad.erase(tmp_rad.begin() + ind);
    tmp_Npart--;

    // Needs re-initialization

    return 0;
}

int commit_particles(){

    tsunami4py->Npart = tmp_Npart;
    tsunami4py->allocate_arrays();
    initialized = true;

    sync_from_interface_to_internals();

    // Rescale to com
    tsunami4py->scale_to_com();
    tsunami4py->initialize_integrator();

    return 0;
}

int recommit_particles() {
    // We are here because something changed.
    bool reallocate = tmp_Npart != tsunami4py->Npart;
    if (reallocate) {
        // Realloacate if particle number has changed
        tsunami4py->deallocate_arrays();
        tsunami4py->Npart = tmp_Npart;
        tsunami4py->allocate_arrays();
    }

    sync_from_interface_to_internals();

    if (reallocate)
        tsunami4py->reset_integrator_changeN();
    else
        tsunami4py->reset_integrator_sameN();

    return 0;
}

int evolve_model(double time){
    return 0;
}

int synchronize_model(){
    return 0;
}

int commit_parameters(){
    return 0;
}

int recommit_parameters(){
    return 0;
}

int set_mass(int index_of_the_particle, double mass) {

    size_t ind = find(tmp_idlist.begin(), tmp_idlist.end(), index_of_the_particle) - tmp_idlist.begin();
    if (ind >= tmp_Npart) {
        return -1;
    }

    if(not initialized) {
        tmp_mass[ind] = mass;
    } else {
        tsunami4py->mass[ind] = mass;
        // Needs reset
    }

    return 0;
}

int get_mass(int index_of_the_particle, double * mass) {

    size_t ind = find(tmp_idlist.begin(), tmp_idlist.end(), index_of_the_particle) - tmp_idlist.begin();
    if (ind >= tmp_Npart) {
        return -1;
    }

    if(not initialized) {
        *mass = tmp_mass[ind];
    } else {
        *mass = tsunami4py->mass[ind];
        // Needs reset
    }

    return 0;
}

int set_radius(int index_of_the_particle, double radius) {

    size_t ind = find(tmp_idlist.begin(), tmp_idlist.end(), index_of_the_particle) - tmp_idlist.begin();
    if (ind >= tmp_Npart) {
        return -1;
    }


    if(not initialized) {
        tmp_rad[ind] = radius;
    } else {
        tsunami4py->rad[ind] = radius;
        // Needs reset
    }

    return 0;
}

int get_radius(int index_of_the_particle, double * radius){

    size_t ind = find(tmp_idlist.begin(), tmp_idlist.end(), index_of_the_particle) - tmp_idlist.begin();
    if (ind >= tmp_Npart) {
        return -1;
    }

    //sync_from_internals_to_interface();
    if(not initialized) {
        *radius = tmp_rad[ind];
    } else {
        *radius = tsunami4py->rad[ind];
    }

    return 0;
}

int set_position(int index_of_the_particle, double x, double y, double z) {

    // Maybe no need
    //sync_from_internals_to_interface();

    size_t ind = find(tmp_idlist.begin(), tmp_idlist.end(), index_of_the_particle) - tmp_idlist.begin();
    if (ind >= tmp_Npart) {
        return -1;
    }
    if(not initialized) {
        tmp_pos[ind].x = x;
        tmp_pos[ind].y = y;
        tmp_pos[ind].z = z;
    } else {
        tsunami4py->pos[ind].x = x;
        tsunami4py->pos[ind].y = y;
        tsunami4py->pos[ind].z = z;
        // Needs reset
    }

    return 0;
}

int get_position(int index_of_the_particle, double * x, double * y, double * z) {

    size_t ind = find(tmp_idlist.begin(), tmp_idlist.end(), index_of_the_particle) - tmp_idlist.begin();
    if (ind >= tmp_Npart) {
        return -1;
    }

    if(not initialized) {
        *x = tmp_pos[ind].x;
        *y = tmp_pos[ind].y;
        *z = tmp_pos[ind].z;
    } else {
        *x = tsunami4py->pos[ind].x;
        *y = tsunami4py->pos[ind].y;
        *z = tsunami4py->pos[ind].z;
    }

    return 0;
}

int set_velocity(int index_of_the_particle, double vx, double vy, double vz) {

    size_t ind = find(tmp_idlist.begin(), tmp_idlist.end(), index_of_the_particle) - tmp_idlist.begin();
    if (ind >= tmp_Npart) {
        return -1;
    }

    if(not initialized) {
        tmp_vel[ind].x = vx;
        tmp_vel[ind].y = vy;
        tmp_vel[ind].z = vz;
    } else {
        tsunami4py->vel[ind].x = vx;
        tsunami4py->vel[ind].y = vy;
        tsunami4py->vel[ind].z = vz;
        // Needs reset
    }

    // Needs reset

    return 0;
}

int get_velocity(int index_of_the_particle, double * vx, double * vy, double * vz) {

    size_t ind = find(tmp_idlist.begin(), tmp_idlist.end(), index_of_the_particle) - tmp_idlist.begin();
    if (ind >= tmp_Npart) {
        return -1;
    }

    if(not initialized) {
        *vx = tmp_vel[ind].x;
        *vy = tmp_vel[ind].y;
        *vz = tmp_vel[ind].z;
    } else {
        *vx = tsunami4py->vel[ind].x;
        *vy = tsunami4py->vel[ind].y;
        *vz = tsunami4py->vel[ind].z;
        // Needs reset
    }

    return 0;
}

int set_state(int index_of_the_particle, double mass, double x, double y,
              double z, double vx, double vy, double vz, double radius) {
    size_t ind = find(tmp_idlist.begin(), tmp_idlist.end(), index_of_the_particle) - tmp_idlist.begin();
    if (ind >= tmp_Npart) {
        return -1;
    }
    if (not initialized) {
        tmp_mass[ind] = mass;
        tmp_rad[ind] = radius;

        tmp_pos[ind].x = x;
        tmp_pos[ind].y = y;
        tmp_pos[ind].z = z;

        tmp_vel[ind].x = vx;
        tmp_vel[ind].y = vy;
        tmp_vel[ind].z = vz;
    } else {
        tsunami4py->mass[ind] = mass;
        tsunami4py->rad[ind] = radius;

        tsunami4py->pos[ind].x = x;
        tsunami4py->pos[ind].y = y;
        tsunami4py->pos[ind].z = z;

        tsunami4py->vel[ind].x = vx;
        tsunami4py->vel[ind].y = vy;
        tsunami4py->vel[ind].z = vz;
        // Needs reset
    }


    return 0;
}

int get_state(int index_of_the_particle, double * mass, double * x,
              double * y, double * z, double * vx, double * vy, double * vz,
              double * radius) {
    size_t ind = find(tmp_idlist.begin(), tmp_idlist.end(), index_of_the_particle) - tmp_idlist.begin();
    if (ind >= tmp_Npart) {
        return -1;
    }

    sync_from_internals_to_interface();

    *mass   = tmp_mass[ind];
    *radius = tmp_rad[ind];

    *x = tmp_pos[ind].x;
    *y = tmp_pos[ind].y;
    *z = tmp_pos[ind].z;

    *vx = tmp_vel[ind].x;
    *vy = tmp_vel[ind].y;
    *vz = tmp_vel[ind].z;

    return 0;
}


int set_begin_time(double time){
    return 0;
}

int get_begin_time(double * time){
    return 0;
}

int set_eps2(double epsilon_squared){
  return 0;
}

int get_eps2(double * epsilon_squared){
  return 0;
}

int get_potential(int index_of_the_particle, double * potential){
  return 0;
}

int set_acceleration(int index_of_the_particle, double ax, double ay,
                     double az){
    return 0;
}

int get_acceleration(int index_of_the_particle, double * ax, double * ay,
                     double * az){
    return 0;
}

int get_number_of_particles(int * number_of_particles){
    if (initialized)
        *number_of_particles = tsunami4py->Npart;
    else
        *number_of_particles = tmp_Npart;

    return 0;
}

int get_index_of_first_particle(int * index_of_the_particle){
    return 0;
}

int get_index_of_next_particle(int index_of_the_particle,
                               int * index_of_the_next_particle){
    return 0;
}

int get_time_step(double * time_step) {
    // Notice: it is previous timestep, not proposed one
    *time_step = tsunami4py->dtphysical;
    return 0;
}

int get_time(double * time) {
    *time = tsunami4py->ctime;
    return 0;
}

int get_total_radius(double * radius){
    return 0;
}

int get_total_mass(double * mass){
    double mtot = 0;
    if (initialized) {
        for (size_t i=0; i<tmp_Npart; i++)
            mtot += tsunami4py->mass[i];
    } else {
        for (size_t i=0; i<tmp_Npart; i++)
            mtot += tmp_mass[i];
    }
    *mass = mtot;

    return 0;
}

int get_kinetic_energy(double * kinetic_energy) {
    *kinetic_energy = tsunami4py->kin;

    return 0;
}

int get_center_of_mass_position(double * x, double * y, double * z){
    // Zero atm
    return 0;
}

int get_center_of_mass_velocity(double * vx, double * vy, double * vz){
    // Zero atm
    return 0;
}

int get_potential_energy(double * potential_energy) {
    *potential_energy = tsunami4py->pot;

    return 0;
}


int echo_int(int int_in, int * int_out){
    cout << int_in;
    *int_out = int_in;
    return 0;
}