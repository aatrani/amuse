#include "worker_code.h"
#include "tsunami4py.h"
#include <algorithm>
#include <cstring>

using std::cout;
using std::endl;

Tsunami *tsunami4py = nullptr;
bool initialized = false;
bool synched = false;

size_t tmp_Npart = 0;

int tmp_new_particle_id = 0;
std::vector<int> tmp_idlist;

std::vector<ch_real> tmp_mass;
std::vector<ch_real> tmp_rad;
std::vector<ch_real3> tmp_pos;
std::vector<ch_real3> tmp_vel;

int sync_from_internals() {
    if(initialized and not synched) {
        //From code into std::vectors
        memcpy(&tmp_mass[0], &tsunami4py->mass[0], sizeof(ch_real)*tsunami4py->Npart);
        memcpy(&tmp_rad[0], &tsunami4py->rad[0], sizeof(ch_real)*tsunami4py->Npart);
        memcpy(&tmp_pos[0], &tsunami4py->pos[0], sizeof(ch_real3)*tsunami4py->Npart);
        memcpy(&tmp_vel[0], &tsunami4py->vel[0], sizeof(ch_real3)*tsunami4py->Npart);

        synched = true;
    }
    return 0;
}

int initialize_code(){
    tsunami4py = new Tsunami();
    return 0;
}

int cleanup_code(){
    delete tsunami4py;
    return 0;
}

int new_particle(int * index_of_the_particle, double mass, double x,
                 double y, double z, double vx, double vy, double vz, double radius){
    tmp_Npart += 1;
    *index_of_the_particle = tmp_new_particle_id;

    tmp_idlist.push_back(tmp_new_particle_id);
    tmp_mass.push_back(mass);
    tmp_rad.push_back(radius);
    tmp_pos.push_back(ch_real3(x,y,z));
    tmp_vel.push_back(ch_real3(vx,vy,vz));

    tmp_new_particle_id += 1;

    return 0;
}

int delete_particle(int index_of_the_particle){
    //sync_from_internals();
    size_t ind = find(tmp_idlist.begin(), tmp_idlist.end(), index_of_the_particle) - tmp_idlist.begin();

    if (ind >= tmp_Npart) {
        return -1;
    }

    tmp_idlist.erase(tmp_idlist.begin() + ind);
    tmp_pos.erase(tmp_pos.begin() + ind);
    tmp_vel.erase(tmp_vel.begin() + ind);
    tmp_mass.erase(tmp_mass.begin() + ind);
    tmp_rad.erase(tmp_rad.begin() + ind);

    return 0;
}

int commit_particles(){
    return 0;
}

int recommit_particles(){
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

int set_mass(int index_of_the_particle, double mass){
    return 0;
}

int get_mass(int index_of_the_particle, double * mass){
  return 0;
}

int set_radius(int index_of_the_particle, double radius){
    return 0;
}

int get_radius(int index_of_the_particle, double * radius){
    return 0;
}

int set_position(int index_of_the_particle, double x, double y, double z){
    return 0;
}

int get_position(int index_of_the_particle, double * x, double * y,
                 double * z) {
    size_t ind = find(tmp_idlist.begin(), tmp_idlist.end(), index_of_the_particle) - tmp_idlist.begin();
    if (ind >= tmp_Npart) {
        return -1;
    }

    sync_from_internals();

    *x = tmp_pos[ind].x;
    *y = tmp_pos[ind].y;
    *z = tmp_pos[ind].z;

    return 0;
}

int set_velocity(int index_of_the_particle, double vx, double vy,
                 double vz){
    return 0;
}

int get_velocity(int index_of_the_particle, double * vx, double * vy,
                 double * vz){
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

int set_state(int index_of_the_particle, double mass, double x, double y, 
              double z, double vx, double vy, double vz, double radius) {
    size_t ind = find(tmp_idlist.begin(), tmp_idlist.end(), index_of_the_particle) - tmp_idlist.begin();
    if (ind >= tmp_Npart) {
        return -1;
    }

    tsunami4py->mass[ind] = mass;
    tmp_rad[ind] = radius;

    tmp_pos[ind].x = x;
    tmp_pos[ind].y = y;
    tmp_pos[ind].z = z;

    tmp_vel[ind].x = vx;
    tmp_vel[ind].y = vy;
    tmp_vel[ind].z = vz;

    return 0;
}

int get_state(int index_of_the_particle, double * mass, double * x, 
              double * y, double * z, double * vx, double * vy, double * vz,
              double * radius) {
    size_t ind = find(tmp_idlist.begin(), tmp_idlist.end(), index_of_the_particle) - tmp_idlist.begin();
    if (ind >= tmp_Npart) {
        return -1;
    }

    sync_from_internals();

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


int get_number_of_particles(int * number_of_particles){
    return 0;
}

int get_index_of_first_particle(int * index_of_the_particle){
    return 0;
}

int get_index_of_next_particle(int index_of_the_particle,
                               int * index_of_the_next_particle){
    return 0;
}

int get_time_step(double * time_step){
  return 0;
}

int get_time(double * time){
    return 0;
}

int get_total_radius(double * radius){
    return 0;
}

int get_total_mass(double * mass){
    return 0;
}

int get_kinetic_energy(double * kinetic_energy){
  return 0;
}

int get_center_of_mass_position(double * x, double * y, double * z){
  return 0;
}

int get_center_of_mass_velocity(double * vx, double * vy, double * vz){
  return 0;
}

int get_potential_energy(double * potential_energy){
  return 0;
}


int echo_int(int int_in, int * int_out){
    cout << int_in;

    return 0;
}