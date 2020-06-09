#include "worker_code.h"
#include "tsunami4py.h"
#include <algorithm>
#include <cstring>
#include <cassert>

using std::cout;
using std::endl;

Tsunami *tsunami4py = nullptr;
bool are_arrays_allocated = false;
bool is_interface_uptodate = false;

size_t tmp_Npart = 0;

int tmp_new_particle_id = 0;
std::vector<int> tmp_idlist;

std::vector<ch_real> tmp_mass;
std::vector<ch_real> tmp_rad;
std::vector<ch_real3> tmp_pos;
std::vector<ch_real3> tmp_vel;
std::vector<ch_real> tmp_soft;

int sync_from_internals_to_interface() {
    if(are_arrays_allocated and not is_interface_uptodate) {
        cout << "sync_from_internals_to_interface" << endl;

        //From code into std::vectors
        memcpy(&tmp_mass[0], &tsunami4py->mass[0], sizeof(ch_real)*tsunami4py->Npart);
        memcpy(&tmp_rad[0], &tsunami4py->rad[0], sizeof(ch_real)*tsunami4py->Npart);
        memcpy(&tmp_pos[0], &tsunami4py->pos[0], sizeof(ch_real3)*tsunami4py->Npart);
        memcpy(&tmp_vel[0], &tsunami4py->vel[0], sizeof(ch_real3)*tsunami4py->Npart);

        // Is it working for real?

        is_interface_uptodate = true;
    }
    return 0;
}

int sync_from_interface_to_internals() {
    assert(are_arrays_allocated); // Just to be sure

    std::copy(tmp_pos.begin(), tmp_pos.end(), tsunami4py->pos);
    std::copy(tmp_vel.begin(), tmp_vel.end(), tsunami4py->vel);
    std::copy(tmp_mass.begin(), tmp_mass.end(), tsunami4py->mass);
    std::copy(tmp_rad.begin(), tmp_rad.end(), tsunami4py->rad);

    for(size_t i = 0; i < tmp_Npart; i++) {
        tsunami4py->soft[i] = 0.0; // Softening zero by default
        //TODO LATER tsunami4py->xdata[i].stype = static_cast<ptype>(stype_in[i]);
    }

    return 0;
}

int initialize_code() {
    cout << "initialize_code" << endl;

    tsunami4py = new Tsunami();
    return 0;
}

int cleanup_code() {
    cout << "cleanup_code" << endl;

    delete tsunami4py;
    are_arrays_allocated = false;
    return 0;
}

int new_particle(int * index_of_the_particle, double mass, double x,
                 double y, double z, double vx, double vy, double vz, double radius){
    cout << "new_particle" << endl;

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
    cout << "delete_particle" << endl;

    // Need to sync so when recomming particles, we can simply update
    sync_from_internals_to_interface();

    size_t ind = find(tmp_idlist.begin(), tmp_idlist.end(), index_of_the_particle) - tmp_idlist.begin();

    if (ind >= tmp_Npart) return -1;


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
    cout << "commit_particles" << endl;

    tsunami4py->Npart = tmp_Npart;
    tsunami4py->allocate_arrays();
    are_arrays_allocated = true;

    sync_from_interface_to_internals();

    // Rescale to com
    tsunami4py->scale_to_com();
    tsunami4py->initialize_integrator();

    return 0;
}

int recommit_particles() {
    cout << "recommit_particles" << endl;
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

int evolve_model(double time) {
    cout << "evolve_model" << endl;

    is_interface_uptodate = false;

    for(size_t i=0; i<tsunami4py->Npart; i++) {
        tsunami4py->pos[i] = ch_real3(0.0);
        tsunami4py->rad[i] = 666;
    }


    return 0;
}

int synchronize_model() {
    cout << "synchronize_model" << endl;

    return 0;
}

int commit_parameters() {
    cout << "commit_parameters" << endl;

    return 0;
}

int recommit_parameters() {
    cout << "recommit_parameters" << endl;

    return 0;
}

int set_mass(int index_of_the_particle, double mass) {
    cout << "set_mass" << endl;

    size_t ind = find(tmp_idlist.begin(), tmp_idlist.end(), index_of_the_particle) - tmp_idlist.begin();
    if (ind >= tmp_Npart) return -1;

    tsunami4py->mass[ind] = mass;
    // Needs reset

    return 0;
}

int get_mass(int index_of_the_particle, double * mass) {
    cout << "get_mass" << endl;

    size_t ind = find(tmp_idlist.begin(), tmp_idlist.end(), index_of_the_particle) - tmp_idlist.begin();
    if (ind >= tmp_Npart) return -1;

    *mass = tsunami4py->mass[ind];
    // Needs reset

    return 0;
}

int set_radius(int index_of_the_particle, double radius) {
    cout << "set_radius" << endl;

    size_t ind = find(tmp_idlist.begin(), tmp_idlist.end(), index_of_the_particle) - tmp_idlist.begin();
    if (ind >= tmp_Npart) return -1;

    tsunami4py->rad[ind] = radius;
    // Needs reset

    return 0;
}

int get_radius(int index_of_the_particle, double * radius){
    cout << "get_radius" << endl;

    size_t ind = find(tmp_idlist.begin(), tmp_idlist.end(), index_of_the_particle) - tmp_idlist.begin();
    if (ind >= tmp_Npart) return -1;


    *radius = tsunami4py->rad[ind];

    return 0;
}

int set_position(int index_of_the_particle, double x, double y, double z) {
    cout << "set_position" << endl;

    size_t ind = find(tmp_idlist.begin(), tmp_idlist.end(), index_of_the_particle) - tmp_idlist.begin();
    if (ind >= tmp_Npart) return -1;


    tsunami4py->pos[ind].x = x;
    tsunami4py->pos[ind].y = y;
    tsunami4py->pos[ind].z = z;
    // Needs reset

    return 0;
}

int get_position(int index_of_the_particle, double * x, double * y, double * z) {
    cout << "get_position" << endl;

    size_t ind = find(tmp_idlist.begin(), tmp_idlist.end(), index_of_the_particle) - tmp_idlist.begin();
    if (ind >= tmp_Npart) return -1;

    *x = tsunami4py->pos[ind].x;
    *y = tsunami4py->pos[ind].y;
    *z = tsunami4py->pos[ind].z;
    // Needs reset

    return 0;
}

int set_velocity(int index_of_the_particle, double vx, double vy, double vz) {
    cout << "set_velocity" << endl;

    size_t ind = find(tmp_idlist.begin(), tmp_idlist.end(), index_of_the_particle) - tmp_idlist.begin();
    if (ind >= tmp_Npart) return -1;

    tsunami4py->vel[ind].x = vx;
    tsunami4py->vel[ind].y = vy;
    tsunami4py->vel[ind].z = vz;
    // Needs reset


    return 0;
}

int get_velocity(int index_of_the_particle, double * vx, double * vy, double * vz) {
    cout << "get_velocity" << endl;

    size_t ind = find(tmp_idlist.begin(), tmp_idlist.end(), index_of_the_particle) - tmp_idlist.begin();
    if (ind >= tmp_Npart) return -1;

    *vx = tsunami4py->vel[ind].x;
    *vy = tsunami4py->vel[ind].y;
    *vz = tsunami4py->vel[ind].z;
    // Needs reset

    return 0;
}

int set_state(int index_of_the_particle, double mass, double x, double y,
              double z, double vx, double vy, double vz, double radius) {
    cout << "set_state" << endl;

    size_t ind = find(tmp_idlist.begin(), tmp_idlist.end(), index_of_the_particle) - tmp_idlist.begin();
    if (ind >= tmp_Npart) return -1;

    tsunami4py->mass[ind] = mass;
    tsunami4py->rad[ind] = radius;

    tsunami4py->pos[ind].x = x;
    tsunami4py->pos[ind].y = y;
    tsunami4py->pos[ind].z = z;

    tsunami4py->vel[ind].x = vx;
    tsunami4py->vel[ind].y = vy;
    tsunami4py->vel[ind].z = vz;
    // Needs reset

    return 0;
}

int get_state(int index_of_the_particle, double * mass, double * x,
              double * y, double * z, double * vx, double * vy, double * vz,
              double * radius) {
    cout << "get_state" << endl;

    size_t ind = find(tmp_idlist.begin(), tmp_idlist.end(), index_of_the_particle) - tmp_idlist.begin();
    if (ind >= tmp_Npart) return -1;

    *mass   = tsunami4py->mass[ind];
    *radius = tsunami4py->rad[ind];

    *x = tsunami4py->pos[ind].x;
    *y = tsunami4py->pos[ind].y;
    *z = tsunami4py->pos[ind].z;

    *vx = tsunami4py->vel[ind].x;
    *vy = tsunami4py->vel[ind].y;
    *vz = tsunami4py->vel[ind].z;

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
    for (size_t i=0; i<tmp_Npart; i++)
        mtot += tmp_mass[i];

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