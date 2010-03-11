! ***********************************************************************
!
!   Copyright (C) 2006, 2007, 2008, 2009  Bill Paxton, Frank Timmes
!
!   This file is part of MESA.
!
!   MESA is free software; you can redistribute it and/or modify
!   it under the terms of the GNU General Library Public License as published
!   by the Free Software Foundation; either version 2 of the License, or
!   (at your option) any later version.
!
!   MESA is distributed in the hope that it will be useful,
!   but WITHOUT ANY WARRANTY; without even the implied warranty of
!   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
!   GNU Library General Public License for more details.
!
!   You should have received a copy of the GNU Library General Public License
!   along with this software; if not, write to the Free Software
!   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
!
! ***********************************************************************

      module eos_def
      implicit none
       
      ! cgs units
      
      ! the basic eos results
      
      integer, parameter :: i_lnPgas = 1
            ! gas pressure (total pressure minus radiation pressure)
      integer, parameter :: i_lnE = 2 
            ! internal energy per gram
      integer, parameter :: i_lnS = 3 
            ! entropy per gram
      integer, parameter :: i_grad_ad = 4 
            ! dlnT_dlnP at constant S
      integer, parameter :: i_chiRho = 5 
            ! dlnP_dlnRho at constant T
      integer, parameter :: i_chiT = 6 
            ! dlnP_dlnT at constant Rho
      integer, parameter :: i_Cp = 7 
            ! dh_dT at constant P, specific heat at constant total pressure
            ! where h is enthalpy, h = E + P/Rho
      integer, parameter :: i_Cv = 8 
            ! dE_dT at constant Rho, specific heat at constant volume
      integer, parameter :: i_dE_dRho = 9 
            ! at constant T
      integer, parameter :: i_dS_dT = 10 
            ! at constant Rho
      integer, parameter :: i_dS_dRho = 11 
            ! at constant T
      integer, parameter :: i_mu = 12 
            ! mean molecular weight per gas particle (ions + free electrons)
      integer, parameter :: i_lnfree_e = 13
            ! mu_e := mean molecular weight per free electron
            ! free_e := 1/mu_e, i.e., mean number of free electrons per nucleon
      integer, parameter :: i_gamma1 = 14 
            ! dlnP_dlnRho at constant S
      integer, parameter :: i_gamma3 = 15 
            ! gamma3 - 1 = dlnT_dlnRho at constant S
      integer, parameter :: i_eta = 16 
            ! electron degeneracy parameter (eta > 1 for significant degeneracy)
            ! eta = ratio of electron chemical potential to kT
      integer, parameter :: i_chiY = 17 
            ! chiY = (dlnP/dlnY) at const T, Rho, and metals; Y = He4 mass fraction
      
      integer, parameter :: num_eos_basic_results = 17

      
      ! NOTE: the calculation of eta is based on the following equation for ne, 
      ! the mean number of free electrons per cm^3,
      ! assuming non-relativistic electrons (okay for T < 10^9 at least)
      !
      !  ne = 4 Pi / h^3 (2 me k T)^1.5 F[1/2,eta]   -- see, for example, Clayton, eqn 2-57
      !        where F is the fermi-dirac integral: 
      !        F[beta,eta] := Integrate[(u^beta)/(1+E^(u-eta)),{u,0,Infinity}]
      ! 
      ! CAVEAT: when free_e, the mean number of free electrons per nucleon gets really small, 
      ! eta isn't very interesting because there aren't a lot of free electrons to be degenerate!
      ! our calculation of eta gets flaky at this point as well.
      ! we sweep this problem under the rug by making eta tend to a fairly large negative value 
      ! when free_e < 0.01 or so. this roughly corresponds to T < 10^4 or less.

      
      integer, parameter :: num_eos_Zs = 3
      double precision, parameter :: eos_Zs(num_eos_Zs) = (/ 0.00d0, 0.02d0, 0.04d0 /)
      
      integer, parameter :: num_eos_Xs = 6
      double precision, parameter :: eos_Xs(num_eos_Xs) =
     >      (/ 0.0d0, 0.2d0, 0.4d0, 0.6d0, 0.8d0, 1.0d0 /)

      integer, parameter :: sz_per_eos_point = 4 ! for bicubic spline interpolation

      type EoS_General_Info
         ! transition temperature zone for OPAL to HELM
         double precision :: logT_all_HELM ! HELM for lgT >= this
         double precision :: logT_all_OPAL ! OPAL for lgT <= this
         ! bookkeeping
         integer :: handle
         logical :: in_use
      end type EoS_General_Info



      ! helm results
      
      integer, parameter ::
     >   h_ptot = 1,
     >   h_dpt = 2,
     >   h_dpd = 3,
     >   h_dpa = 4,
     >   h_dpz = 5,
     >   h_dpdd = 6,
     >   h_dpdt = 7,
     >   h_dpda = 8,
     >   h_dpdz = 9,
     >   h_dptt = 10,
     >   h_dpta = 11,
     >   h_dptz = 12,
     >   h_dpaa = 13,
     >   h_dpaz = 14,
     >   h_dpzz = 15
         
      integer, parameter ::
     >   x_p = 15

      integer, parameter ::
     >   h_etot = x_p + 1,
     >   h_det = x_p + 2,
     >   h_ded = x_p + 3,
     >   h_dea = x_p + 4,
     >   h_dez = x_p + 5,
     >   h_dedd = x_p + 6,
     >   h_dedt = x_p + 7,
     >   h_deda = x_p + 8,
     >   h_dedz = x_p + 9,
     >   h_dett = x_p + 10,
     >   h_deta = x_p + 11,
     >   h_detz = x_p + 12,
     >   h_deaa = x_p + 13,
     >   h_deaz = x_p + 14,
     >   h_dezz = x_p + 15
         
      integer, parameter ::
     >   x_e = x_p + 15

      integer, parameter ::
     >   h_stot = x_e + 1,
     >   h_dst = x_e + 2,
     >   h_dsd = x_e + 3,
     >   h_dsa = x_e + 4,
     >   h_dsz = x_e + 5,
     >   h_dsdd = x_e + 6,
     >   h_dsdt = x_e + 7,
     >   h_dsda = x_e + 8,
     >   h_dsdz = x_e + 9,
     >   h_dstt = x_e + 10,
     >   h_dsta = x_e + 11,
     >   h_dstz = x_e + 12,
     >   h_dsaa = x_e + 13,
     >   h_dsaz = x_e + 14,
     >   h_dszz = x_e + 15
         
      integer, parameter ::
     >   x_s = x_e + 15


      !..radiation contributions 
      integer, parameter ::
     >   h_prad = x_s + 1,
     >   h_dpradt = x_s + 2,
     >   h_dpradd = x_s + 3,
     >   h_dprada = x_s + 4,
     >   h_dpradz = x_s + 5,
     >   h_dpraddd = x_s + 6,
     >   h_dpraddt = x_s + 7,
     >   h_dpradda = x_s + 8,
     >   h_dpraddz = x_s + 9,
     >   h_dpradtt = x_s + 10,
     >   h_dpradta = x_s + 11,
     >   h_dpradtz = x_s + 12,
     >   h_dpradaa = x_s + 13,
     >   h_dpradaz = x_s + 14,
     >   h_dpradzz = x_s + 15
         
      integer, parameter ::
     >   x_pr = x_s + 15


      integer, parameter ::
     >   h_erad = x_pr + 1,
     >   h_deradt = x_pr + 2,
     >   h_deradd = x_pr + 3,
     >   h_derada = x_pr + 4,
     >   h_deradz = x_pr + 5,
     >   h_deraddd = x_pr + 6,
     >   h_deraddt = x_pr + 7,
     >   h_deradda = x_pr + 8,
     >   h_deraddz = x_pr + 9,
     >   h_deradtt = x_pr + 10,
     >   h_deradta = x_pr + 11,
     >   h_deradtz = x_pr + 12,
     >   h_deradaa = x_pr + 13,
     >   h_deradaz = x_pr + 14,
     >   h_deradzz = x_pr + 15
         
      integer, parameter ::
     >   x_er = x_pr + 15


      integer, parameter ::
     >   h_srad = x_er + 1,
     >   h_dsradt = x_er + 2,
     >   h_dsradd = x_er + 3,
     >   h_dsrada = x_er + 4,
     >   h_dsradz = x_er + 5,
     >   h_dsraddd = x_er + 6,
     >   h_dsraddt = x_er + 7,
     >   h_dsradda = x_er + 8,
     >   h_dsraddz = x_er + 9,
     >   h_dsradtt = x_er + 10,
     >   h_dsradta = x_er + 11,
     >   h_dsradtz = x_er + 12,
     >   h_dsradaa = x_er + 13,
     >   h_dsradaz = x_er + 14,
     >   h_dsradzz = x_er + 15
         
      integer, parameter ::
     >   x_sr = x_er + 15



      !..gas contributions 
      integer, parameter ::
     >   h_pgas = x_sr + 1,
     >   h_dpgast = x_sr + 2,
     >   h_dpgasd = x_sr + 3,
     >   h_dpgasa = x_sr + 4,
     >   h_dpgasz = x_sr + 5,
     >   h_dpgasdd = x_sr + 6,
     >   h_dpgasdt = x_sr + 7,
     >   h_dpgasda = x_sr + 8,
     >   h_dpgasdz = x_sr + 9,
     >   h_dpgastt = x_sr + 10,
     >   h_dpgasta = x_sr + 11,
     >   h_dpgastz = x_sr + 12,
     >   h_dpgasaa = x_sr + 13,
     >   h_dpgasaz = x_sr + 14,
     >   h_dpgaszz = x_sr + 15
         
      integer, parameter ::
     >   x_pg = x_sr + 15


      integer, parameter ::
     >   h_egas = x_pg + 1,
     >   h_degast = x_pg + 2,
     >   h_degasd = x_pg + 3,
     >   h_degasa = x_pg + 4,
     >   h_degasz = x_pg + 5,
     >   h_degasdd = x_pg + 6,
     >   h_degasdt = x_pg + 7,
     >   h_degasda = x_pg + 8,
     >   h_degasdz = x_pg + 9,
     >   h_degastt = x_pg + 10,
     >   h_degasta = x_pg + 11,
     >   h_degastz = x_pg + 12,
     >   h_degasaa = x_pg + 13,
     >   h_degasaz = x_pg + 14,
     >   h_degaszz = x_pg + 15
         
      integer, parameter ::
     >   x_eg = x_pg + 15


      integer, parameter ::
     >   h_sgas = x_eg + 1,
     >   h_dsgast = x_eg + 2,
     >   h_dsgasd = x_eg + 3,
     >   h_dsgasa = x_eg + 4,
     >   h_dsgasz = x_eg + 5,
     >   h_dsgasdd = x_eg + 6,
     >   h_dsgasdt = x_eg + 7,
     >   h_dsgasda = x_eg + 8,
     >   h_dsgasdz = x_eg + 9,
     >   h_dsgastt = x_eg + 10,
     >   h_dsgasta = x_eg + 11,
     >   h_dsgastz = x_eg + 12,
     >   h_dsgasaa = x_eg + 13,
     >   h_dsgasaz = x_eg + 14,
     >   h_dsgaszz = x_eg + 15
         
      integer, parameter ::
     >   x_sg = x_eg + 15


      !..ion contributions
      integer, parameter ::
     >   h_pion = x_sg + 1,
     >   h_dpiont = x_sg + 2,
     >   h_dpiond = x_sg + 3,
     >   h_dpiona = x_sg + 4,
     >   h_dpionz = x_sg + 5,
     >   h_dpiondd = x_sg + 6,
     >   h_dpiondt = x_sg + 7,
     >   h_dpionda = x_sg + 8,
     >   h_dpiondz = x_sg + 9,
     >   h_dpiontt = x_sg + 10,
     >   h_dpionta = x_sg + 11,
     >   h_dpiontz = x_sg + 12,
     >   h_dpionaa = x_sg + 13,
     >   h_dpionaz = x_sg + 14,
     >   h_dpionzz = x_sg + 15
         
      integer, parameter ::
     >   x_pi = x_sg + 15


      integer, parameter ::
     >   h_eion = x_pi + 1,
     >   h_deiont = x_pi + 2,
     >   h_deiond = x_pi + 3,
     >   h_deiona = x_pi + 4,
     >   h_deionz = x_pi + 5,
     >   h_deiondd = x_pi + 6,
     >   h_deiondt = x_pi + 7,
     >   h_deionda = x_pi + 8,
     >   h_deiondz = x_pi + 9,
     >   h_deiontt = x_pi + 10,
     >   h_deionta = x_pi + 11,
     >   h_deiontz = x_pi + 12,
     >   h_deionaa = x_pi + 13,
     >   h_deionaz = x_pi + 14,
     >   h_deionzz = x_pi + 15
         
      integer, parameter ::
     >   x_ei = x_pi + 15


      integer, parameter ::
     >   h_sion = x_ei + 1,
     >   h_dsiont = x_ei + 2,
     >   h_dsiond = x_ei + 3,
     >   h_dsiona = x_ei + 4,
     >   h_dsionz = x_ei + 5,
     >   h_dsiondd = x_ei + 6,
     >   h_dsiondt = x_ei + 7,
     >   h_dsionda = x_ei + 8,
     >   h_dsiondz = x_ei + 9,
     >   h_dsiontt = x_ei + 10,
     >   h_dsionta = x_ei + 11,
     >   h_dsiontz = x_ei + 12,
     >   h_dsionaa = x_ei + 13,
     >   h_dsionaz = x_ei + 14,
     >   h_dsionzz = x_ei + 15
         
      integer, parameter ::
     >   x_si = x_ei + 15

      integer, parameter ::
     >   h_etaion = x_si + 1,
     >   h_detait = x_si + 2,
     >   h_detaid = x_si + 3,
     >   h_detaia = x_si + 4,
     >   h_detaiz = x_si + 5,
     >   h_detaidd = x_si + 6,
     >   h_detaidt = x_si + 7,
     >   h_detaida = x_si + 8,
     >   h_detaidz = x_si + 9,
     >   h_detaitt = x_si + 10,
     >   h_detaita = x_si + 11,
     >   h_detaitz = x_si + 12,
     >   h_detaiaa = x_si + 13,
     >   h_detaiaz = x_si + 14,
     >   h_detaizz = x_si + 15
         
      integer, parameter ::
     >   x_etai = x_si + 15


      integer, parameter ::
     >   h_xni = x_etai + 1,
     >   h_dxnit = x_etai + 2,
     >   h_dxnid = x_etai + 3,
     >   h_dxnia = x_etai + 4,
     >   h_dxniz = x_etai + 5,
     >   h_dxnidd = x_etai + 6,
     >   h_dxnidt = x_etai + 7,
     >   h_dxnida = x_etai + 8,
     >   h_dxnidz = x_etai + 9,
     >   h_dxnitt = x_etai + 10,
     >   h_dxnita = x_etai + 11,
     >   h_dxnitz = x_etai + 12,
     >   h_dxniaa = x_etai + 13,
     >   h_dxniaz = x_etai + 14,
     >   h_dxnizz = x_etai + 15
         
      integer, parameter ::
     >   x_xni = x_etai + 15


      !..electron-positron contributions 

      integer, parameter ::
     >   h_etaele = x_xni + 1,
     >   h_etapos = x_xni + 2,
     >   h_detat = x_xni + 3,
     >   h_detad = x_xni + 4,
     >   h_detaa = x_xni + 5,
     >   h_detaz = x_xni + 6,
     >   h_detadd = x_xni + 7,
     >   h_detadt = x_xni + 8,
     >   h_detada = x_xni + 9,
     >   h_detadz = x_xni + 10,
     >   h_detatt = x_xni + 11,
     >   h_detata = x_xni + 12,
     >   h_detatz = x_xni + 13,
     >   h_detaaa = x_xni + 14,
     >   h_detaaz = x_xni + 15,
     >   h_detazz = x_xni + 16
         
      integer, parameter ::
     >   x_etae = x_xni + 16

      integer, parameter ::
     >   h_pele = x_etae + 1,
     >   h_ppos = x_etae + 2,
     >   h_dpept = x_etae + 3,
     >   h_dpepd = x_etae + 4,
     >   h_dpepa = x_etae + 5,
     >   h_dpepz = x_etae + 6,
     >   h_dpepdd = x_etae + 7,
     >   h_dpepdt = x_etae + 8,
     >   h_dpepda = x_etae + 9,
     >   h_dpepdz = x_etae + 10,
     >   h_dpeptt = x_etae + 11,
     >   h_dpepta = x_etae + 12,
     >   h_dpeptz = x_etae + 13,
     >   h_dpepaa = x_etae + 14,
     >   h_dpepaz = x_etae + 15,
     >   h_dpepzz = x_etae + 16
         
      integer, parameter ::
     >   x_pep = x_etae + 16


      integer, parameter ::
     >   h_eele = x_pep + 1,
     >   h_epos = x_pep + 2,
     >   h_deept = x_pep + 3,
     >   h_deepd = x_pep + 4,
     >   h_deepa = x_pep + 5,
     >   h_deepz = x_pep + 6,
     >   h_deepdd = x_pep + 7,
     >   h_deepdt = x_pep + 8,
     >   h_deepda = x_pep + 9,
     >   h_deepdz = x_pep + 10,
     >   h_deeptt = x_pep + 11,
     >   h_deepta = x_pep + 12,
     >   h_deeptz = x_pep + 13,
     >   h_deepaa = x_pep + 14,
     >   h_deepaz = x_pep + 15,
     >   h_deepzz = x_pep + 16
         
      integer, parameter ::
     >   x_eep = x_pep + 16


      integer, parameter ::
     >   h_sele = x_eep + 1,
     >   h_spos = x_eep + 2,
     >   h_dsept = x_eep + 3,
     >   h_dsepd = x_eep + 4,
     >   h_dsepa = x_eep + 5,
     >   h_dsepz = x_eep + 6,
     >   h_dsepdd = x_eep + 7,
     >   h_dsepdt = x_eep + 8,
     >   h_dsepda = x_eep + 9,
     >   h_dsepdz = x_eep + 10,
     >   h_dseptt = x_eep + 11,
     >   h_dsepta = x_eep + 12,
     >   h_dseptz = x_eep + 13,
     >   h_dsepaa = x_eep + 14,
     >   h_dsepaz = x_eep + 15,
     >   h_dsepzz = x_eep + 16
         
      integer, parameter ::
     >   x_sep = x_eep + 16


      integer, parameter ::
     >   h_xne = x_sep + 1,
     >   h_xnp = x_sep + 2,
     >   h_xnem = x_sep + 3,
     >   h_dxnet = x_sep + 4,
     >   h_dxned = x_sep + 5,
     >   h_dxnea = x_sep + 6,
     >   h_dxnez = x_sep + 7,
     >   h_dxnedd = x_sep + 8,
     >   h_dxnedt = x_sep + 9,
     >   h_dxneda = x_sep + 10,
     >   h_dxnedz = x_sep + 11,
     >   h_dxnett = x_sep + 12,
     >   h_dxneta = x_sep + 13,
     >   h_dxnetz = x_sep + 14,
     >   h_dxneaa = x_sep + 15,
     >   h_dxneaz = x_sep + 16,
     >   h_dxnezz = x_sep + 17
         
      integer, parameter ::
     >   x_xne = x_sep + 17


      !..ionization potential contributions
      integer, parameter ::
     >   h_pip = x_xne + 1,
     >   h_eip = x_xne + 2,
     >   h_sip = x_xne + 3
         
      integer, parameter ::
     >   x_ip = x_xne + 3


      !..coulomb contributions
      integer, parameter ::
     >   h_pcou = x_ip + 1,
     >   h_dpcout = x_ip + 2,
     >   h_dpcoud = x_ip + 3,
     >   h_dpcoua = x_ip + 4,
     >   h_dpcouz = x_ip + 5,
     >   h_ecou = x_ip + 6,
     >   h_decout = x_ip + 7,
     >   h_decoud = x_ip + 8,
     >   h_decoua = x_ip + 9,
     >   h_decouz = x_ip + 10,
     >   h_scou = x_ip + 11,
     >   h_dscout = x_ip + 12,
     >   h_dscoud = x_ip + 13,
     >   h_dscoua = x_ip + 14,
     >   h_dscouz = x_ip + 15,
     >   h_plasg = x_ip + 16
         
      integer, parameter ::
     >   x_cou = x_ip + 16


      !..thermodynamic consistency checks; maxwell relations 
      integer, parameter ::
     >   h_dse = x_cou + 1,
     >   h_dpe = x_cou + 2,
     >   h_dsp = x_cou + 3
         
      integer, parameter ::
     >   x_mxwll = x_cou + 3


      !..derivative based quantities for the gas
      integer, parameter ::
     >   h_cp_gas = x_mxwll + 1,
     >   h_dcp_gasdd = x_mxwll + 2,
     >   h_dcp_gasdt = x_mxwll + 3,
     >   h_dcp_gasda = x_mxwll + 4,
     >   h_dcp_gasdz = x_mxwll + 5,
     >   h_cv_gas = x_mxwll + 6,
     >   h_dcv_gasdd = x_mxwll + 7,
     >   h_dcv_gasdt = x_mxwll + 8,
     >   h_dcv_gasda = x_mxwll + 9,
     >   h_dcv_gasdz = x_mxwll + 10,
     >   h_gam1_gas = x_mxwll + 11,
     >   h_dgam1_gasdd = x_mxwll + 12,
     >   h_dgam1_gasdt = x_mxwll + 13,
     >   h_dgam1_gasda = x_mxwll + 14,
     >   h_dgam1_gasdz = x_mxwll + 15,
     >   h_gam2_gas = x_mxwll + 16,
     >   h_dgam2_gasdd = x_mxwll + 17,
     >   h_dgam2_gasdt = x_mxwll + 18,
     >   h_dgam2_gasda = x_mxwll + 19,
     >   h_dgam2_gasdz = x_mxwll + 20,
     >   h_gam3_gas = x_mxwll + 21,
     >   h_dgam3_gasdd = x_mxwll + 22,
     >   h_dgam3_gasdt = x_mxwll + 23,
     >   h_dgam3_gasda = x_mxwll + 24,
     >   h_dgam3_gasdz = x_mxwll + 25,
     >   h_nabad_gas = x_mxwll + 26,
     >   h_dnab_gasdd = x_mxwll + 27,
     >   h_dnab_gasdt = x_mxwll + 28,
     >   h_dnab_gasda = x_mxwll + 29,
     >   h_dnab_gasdz = x_mxwll + 30,
     >   h_cs_gas = x_mxwll + 31,
     >   h_dcs_gasdd = x_mxwll + 32,
     >   h_dcs_gasdt = x_mxwll + 33,
     >   h_dcs_gasda = x_mxwll + 34,
     >   h_dcs_gasdz = x_mxwll + 35
         
      integer, parameter ::
     >   x_dgas = x_mxwll + 35


      !..derivative based quantities for the totals
      integer, parameter ::
     >   h_cp = x_dgas + 1,
     >   h_dcpdd = x_dgas + 2,
     >   h_dcpdt = x_dgas + 3,
     >   h_dcpda = x_dgas + 4,
     >   h_dcpdz = x_dgas + 5,
     >   h_cv = x_dgas + 6,
     >   h_dcvdd = x_dgas + 7,
     >   h_dcvdt = x_dgas + 8,
     >   h_dcvda = x_dgas + 9,
     >   h_dcvdz = x_dgas + 10,
     >   h_gam1 = x_dgas + 11,
     >   h_dgam1dd = x_dgas + 12,
     >   h_dgam1dt = x_dgas + 13,
     >   h_dgam1da = x_dgas + 14,
     >   h_dgam1dz = x_dgas + 15,
     >   h_gam2 = x_dgas + 16,
     >   h_dgam2dd = x_dgas + 17,
     >   h_dgam2dt = x_dgas + 18,
     >   h_dgam2da = x_dgas + 19,
     >   h_dgam2dz = x_dgas + 20,
     >   h_gam3 = x_dgas + 21,
     >   h_dgam3dd = x_dgas + 22,
     >   h_dgam3dt = x_dgas + 23,
     >   h_dgam3da = x_dgas + 24,
     >   h_dgam3dz = x_dgas + 25,
     >   h_nabad = x_dgas + 26,
     >   h_dnabdd = x_dgas + 27,
     >   h_dnabdt = x_dgas + 28,
     >   h_dnabda = x_dgas + 29,
     >   h_dnabdz = x_dgas + 30,
     >   h_cs = x_dgas + 31,
     >   h_dcsdd = x_dgas + 32,
     >   h_dcsdt = x_dgas + 33,
     >   h_dcsda = x_dgas + 34,
     >   h_dcsdz = x_dgas + 35,
     >   h_chit = x_dgas + 36,
     >   h_dchitdd = x_dgas + 37,
     >   h_dchitdt = x_dgas + 38,
     >   h_dchitda = x_dgas + 39,
     >   h_dchitdz = x_dgas + 40,
     >   h_chid = x_dgas + 41,
     >   h_dchiddd = x_dgas + 42,
     >   h_dchiddt = x_dgas + 43,
     >   h_dchidda = x_dgas + 44,
     >   h_dchiddz = x_dgas + 45,
     >   h_chiY = x_dgas + 46
         
      integer, parameter ::
     >   x_dtot = x_dgas + 46
         

      !  random cr.p for debugging
      integer, parameter ::
     >   h_crp = x_dtot + 1,
     >   h_dcrpt = x_dtot + 2,
     >   h_dcrpd = x_dtot + 3,
     >   h_dcrpa = x_dtot + 4,
     >   h_dcrpz = x_dtot + 5,
     >   h_dcrpdd = x_dtot + 6,
     >   h_dcrpdt = x_dtot + 7,
     >   h_dcrpda = x_dtot + 8,
     >   h_dcrpdz = x_dtot + 9,
     >   h_dcrptt = x_dtot + 10,
     >   h_dcrpta = x_dtot + 11,
     >   h_dcrptz = x_dtot + 12,
     >   h_dcrpaa = x_dtot + 13,
     >   h_dcrpaz = x_dtot + 14,
     >   h_dcrpzz = x_dtot + 15
     
     
      ! validity flag
      ! nonzero if the previous entries were actually computed by helm
      ! zero if we didn't call helm 
      integer, parameter :: h_valid = h_dcrpzz + 1

         
      integer, parameter :: num_helm_results = h_valid

      ! end helm results


      ! the following is private info for helm
      
      type Helm_Table
      
         ! controls
         logical :: with_coulomb_corrections
      
         ! sizes of the arrays
         integer :: imax
         integer :: jmax

         !..density and temperature
         double precision :: logtlo ! log10 temp
         double precision :: logthi ! log10 temp
         double precision :: templo ! 10**logtlo
         double precision :: temphi ! 10**logthi
         double precision :: logtstp
         double precision :: logtstpi
         double precision :: logdlo ! log10 rho
         double precision :: logdhi ! log10 rho
         double precision :: denlo ! 10**logdlo
         double precision :: denhi ! 10**logdhi
         double precision :: logdstp
         double precision :: logdstpi
         double precision, dimension(:), pointer :: d ! (imax) 
         double precision, dimension(:), pointer :: t ! (jmax) 

         !..for the helmholtz free energy tables
         double precision, dimension(:,:), pointer :: f ! (imax,jmax) 
         double precision, dimension(:,:), pointer :: fd ! (imax,jmax)
         double precision, dimension(:,:), pointer :: ft ! (imax,jmax)
         double precision, dimension(:,:), pointer :: fdd ! (imax,jmax)
         double precision, dimension(:,:), pointer :: ftt ! (imax,jmax)
         double precision, dimension(:,:), pointer :: fdt ! (imax,jmax)
         double precision, dimension(:,:), pointer :: fddt ! (imax,jmax)
         double precision, dimension(:,:), pointer :: fdtt ! (imax,jmax)
         double precision, dimension(:,:), pointer :: fddtt ! (imax,jmax)

         !..for the pressure derivative with density tables
         double precision, dimension(:,:), pointer :: dpdf ! (imax,jmax)
         double precision, dimension(:,:), pointer :: dpdfd ! (imax,jmax)
         double precision, dimension(:,:), pointer :: dpdft ! (imax,jmax)
         double precision, dimension(:,:), pointer :: dpdfdt ! (imax,jmax)

         !..for chemical potential tables
         double precision, dimension(:,:), pointer :: ef ! (imax,jmax)
         double precision, dimension(:,:), pointer :: efd ! (imax,jmax)
         double precision, dimension(:,:), pointer :: eft ! (imax,jmax)
         double precision, dimension(:,:), pointer :: efdt ! (imax,jmax)

         !..for the number density tables
         double precision, dimension(:,:), pointer :: xf ! (imax,jmax)
         double precision, dimension(:,:), pointer :: xfd ! (imax,jmax)
         double precision, dimension(:,:), pointer :: xft ! (imax,jmax)
         double precision, dimension(:,:), pointer :: xfdt ! (imax,jmax)

         !..for storing the differences
         double precision, dimension(:), pointer :: dt_sav ! (jmax)
         double precision, dimension(:), pointer :: dt2_sav ! (jmax)
         double precision, dimension(:), pointer :: dti_sav ! (jmax)
         double precision, dimension(:), pointer :: dt2i_sav ! (jmax)
         double precision, dimension(:), pointer :: dt3i_sav ! (jmax)
         double precision, dimension(:), pointer :: dd_sav ! (imax)
         double precision, dimension(:), pointer :: dd2_sav ! (imax)
         double precision, dimension(:), pointer :: ddi_sav ! (imax)
         double precision, dimension(:), pointer :: dd2i_sav ! (imax)
         double precision, dimension(:), pointer :: dd3i_sav ! (jmax)

      end type Helm_Table



      ! THE FOLLOWING ARE PRIVATE DEFS -- NOT FOR USE BY CLIENTS
      

      type (Helm_Table), pointer :: eos_ht ! currently, we just have one copy of the Helm_Table
         ! it is "read-only" after initialization.
      
      
      ! for eosDT

      real :: eosDT_logQ_min ! logQ = logRho - 2*logT + 12
      real :: eosDT_logQ_max
      real :: eosDT_del_logQ ! spacing for the logQs
      integer :: eosDT_num_logQs
      real :: eosDT_logT_min
      real :: eosDT_logT_max
      real :: eosDT_del_logT ! spacing for the logTs
      integer :: eosDT_num_logTs
      real, dimension(:,:,:,:,:,:), pointer :: eosDT_tbl
         ! dimension(sz_per_eos_point, num_eos_vals, num_logQs, num_logTs, num_eos_Xs, num_eos_Zs)

      ! internal storage of table info
      integer, parameter :: eosDT_ilnE = 1
      integer, parameter :: eosDT_ilnPgas = 2
      ! the rest are the same for all of the cases
      integer, parameter :: eos_ilnS = 3
      integer, parameter :: eos_igrad_ad = 4
      integer, parameter :: eos_ichiRho = 5
      integer, parameter :: eos_ichiT = 6
      integer, parameter :: eos_iCp = 7
      integer, parameter :: eos_iCv = 8
      integer, parameter :: eos_idE_dRho = 9
      integer, parameter :: eos_idS_dT = 10
      integer, parameter :: eos_idS_dRho = 11
      integer, parameter :: eos_imu = 12
      integer, parameter :: eos_ilnfree_e = 13
      integer, parameter :: eos_igamma1 = 14
      integer, parameter :: eos_igamma3 = 15
      integer, parameter :: eos_ieta = 16
      integer, parameter :: eos_ichiY = 17

      integer, parameter :: num_eos_vals = 17

      ! we are storing more than we'd need to store if we had unlimited numerical precision.
      ! for example, Cv, the S derivatives, and the gammas can all be derived from the other stuff.
      ! better to be safe, we'll take the storage hit and do them independently.

      
      ! for eosPT
      integer, parameter :: eosPT_ilnE = 1
      integer, parameter :: eosPT_ilnRho = 2

      real :: eosPT_logW_min ! logW = logPgas - 4*logT
      real :: eosPT_logW_max
      real :: eosPT_del_logW ! spacing for the logWs
      integer :: eosPT_num_logWs
      real :: eosPT_logT_min
      real :: eosPT_logT_max
      real :: eosPT_del_logT ! spacing for the logTs
      integer :: eosPT_num_logTs
      real, dimension(:,:,:,:,:,:), pointer :: eosPT_tbl
         ! dimension(sz_per_eos_point, num_eos_vals, num_logWs, num_logTs, num_eos_Xs, num_eos_Zs)

      
      ! for eosDE
      integer, parameter :: eosDE_ilnPgas = 1
      integer, parameter :: eosDE_ilnT = 2

      ! the internal eosDE data
      real :: eosDE_logV_min ! logV = logRho - 3*logE + 45
      real :: eosDE_logV_max
      real :: eosDE_del_logV ! spacing for the logVs
      integer :: eosDE_num_logVs
      real :: eosDE_logRho_min
      real :: eosDE_logRho_max
      real :: eosDE_del_logRho ! spacing for the logRhos
      integer :: eosDE_num_logRhos
      real, dimension(:,:,:,:,:,:), pointer :: eosDE_tbl
         ! dimension(sz_per_eos_point, num_eos_vals, num_logVs, num_logRhos, num_eos_Xs, num_eos_Zs)

      
      ! for eosDP
      integer, parameter :: eosDP_ilnE = 1
      integer, parameter :: eosDP_ilnT = 2

      ! the internal eosDP data
      real :: eosDP_logB_min ! logB = logRho - 0.7*logPgas + 10
      real :: eosDP_logB_max
      real :: eosDP_del_logB ! spacing for the logBs
      integer :: eosDP_num_logBs
      real :: eosDP_logRho_min
      real :: eosDP_logRho_max
      real :: eosDP_del_logRho ! spacing for the logRhos
      integer :: eosDP_num_logRhos
      real, dimension(:,:,:,:,:,:), pointer :: eosDP_tbl
         ! dimension(sz_per_eos_point, num_eos_vals, num_logBs, num_logRhos, num_eos_Xs, num_eos_Zs)
      
      


      ! interpolation info for theta_e
      integer :: theta_e_nx
      double precision, pointer :: f_theta_e(:,:)
      double precision, pointer :: x_theta_e(:)
      
      
      integer, parameter :: max_eos_handles = 1000
      type (EoS_General_Info), target :: eos_handles(max_eos_handles)
      
      
      logical :: use_cache_for_eos
      logical :: eos_root_is_initialized = .false.
      logical :: eosDT_is_initialized = .false.
      logical :: eosPT_is_initialized = .false.
      logical :: eosDE_is_initialized = .false.
      logical :: eosDP_is_initialized = .false.
      
      character(len=256) :: data_dir_for_eos
      
      contains
      
      
      subroutine eos_def_init
         integer :: i
         do i=1,max_eos_handles
            eos_handles(i)% handle = i
            eos_handles(i)% in_use = .false.
         end do
         eos_root_is_initialized = .false.
         eosDT_is_initialized = .false.
         eosPT_is_initialized = .false.
         eosDE_is_initialized = .false.
         eosDP_is_initialized = .false.
         use_cache_for_eos = .true.
      end subroutine eos_def_init

      
      integer function do_alloc_eos(ierr)
         use alert_lib,only:alert
         integer, intent(out) :: ierr
         integer :: i
         type (EoS_General_Info), pointer :: rq
         ierr = 0
         do_alloc_eos = -1
!$omp critical (eos_handle)
         do i = 1, max_eos_handles
            if (.not. eos_handles(i)% in_use) then
               eos_handles(i)% in_use = .true.
               do_alloc_eos = i
               exit
            end if
         end do
!$omp end critical (eos_handle)
         if (do_alloc_eos == -1) then
            ierr = -1
            call alert(ierr, 'no available eos handle')
            return
         end if
         if (eos_handles(do_alloc_eos)% handle /= do_alloc_eos) then
            ierr = -1
            call alert(ierr, 'broken handle for eos')
            return
         end if
         rq => eos_handles(do_alloc_eos)
         rq% logT_all_HELM = 7.7d0
         rq% logT_all_OPAL = 7.6d0
      end function do_alloc_eos
      
      
      subroutine do_free_eos_handle(handle)
         integer, intent(in) :: handle
         type (EoS_General_Info), pointer :: rq
         if (handle >= 1 .and. handle <= max_eos_handles) then
            rq => eos_handles(handle)
            eos_handles(handle)% in_use = .false.
         end if
      end subroutine do_free_eos_handle
      

      subroutine get_eos_ptr(handle,rq,ierr)
         use alert_lib,only:alert
         integer, intent(in) :: handle
         type (EoS_General_Info), pointer :: rq
         integer, intent(out):: ierr         
         if (handle < 1 .or. handle > max_eos_handles) then
            ierr = -1
            call alert(ierr,'invalid eos handle')
            return
         end if
         rq => eos_handles(handle)
         ierr = 0
      end subroutine get_eos_ptr
      

      end module eos_def
      
