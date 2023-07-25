# Basic Hall-Heroult model
import numpy as np
import math

#cell_current
cell_current = 210#kA
ACD = 5.2#cm


#bath data
T_c = 963.3
T_bath_k = T_c + 273.15
w_Al2O3 = 2.5
w_AlF3 = 11
w_CaF2 = 4.5
w_MgF2 = 0.3
w_KF = 0.1
w_LiF = 0.5
CR=2.5

#gas bubbles
thk_bubble = 1.0#cm



#anode data#Dupuis doi:10.1007/978-3-319-51541-0_85
new_anode_width = 1.450#m
new_anode_length = 0.540#m
n_anodes = 32



def bath_k_ckv_eq(T_bath_c, w_AlF3, w_LiF, w_Al2O3):# bath conductivity Chrenkova et. eal eq. Density, Electrical Conductivity And VIscosity Of Low Melting Baths For Aluminum Electrolysis
    bath_k = -7.332 + 1.742e-2 * T_bath_c - 7.313e-6 * pow(T_bath_c, 2) - 1.866e-4 * pow(w_AlF3, 2) - 2.824e-5 * w_AlF3 * T_bath_c + \
             4.613e-2 * w_LiF + 2.046e-4 * pow(w_LiF, 2) - 4.695e-5 * w_Al2O3 * T_bath_c + 2.462e-4 * w_AlF3 * w_LiF + 2.003e-3 * w_AlF3 * w_Al2O3 - \
             5.546e-5 * w_AlF3 * w_LiF * w_Al2O3
    return bath_k

def bath_k_arkp_eq(T_bath_k,w_Al2O3, w_CaF2, CR):
    bath_k = -1.87 + 3.23e-3 *  T_bath_k - 2.99e-2 * w_Al2O3 + 4.70e-1 * CR - 4.37e-2 * w_CaF2
    return bath_k

def bath_k_hives_eq(T_bath_k, w_AlF3, w_Al2O3, w_CaF2, w_MgF2, w_KF, w_LiF):#Hives eq https://doi.org/10.1007/BF02915051
    bath_k = 7.22 * math.exp(-1204.3/T_bath_k) - 2.53 * w_Al2O3 - 1.66 * w_AlF3 - 0.76 * w_CaF2 #- 0.206 * w_KF + 0.97 * w_Li3AlF6
    bath_k = math.exp(1.977 - 0.02 * w_Al2O3 - 0.0131 * w_AlF3 - 0.006 * w_CaF2 - 0.0106 * w_MgF2 - 0.0019 * w_KF + 0.0121 * w_LiF - 1204.3/T_bath_k)
    return bath_k

def anode_surface(anode_width, anode_length, n_anodes):
    new_anodic_surface = anode_width * anode_length * n_anodes
    return new_anodic_surface
new_anodic_surface = anode_surface(anode_width=new_anode_width, anode_length=new_anode_length, n_anodes=n_anodes)
i_a = (cell_current*1000)/(new_anodic_surface*10000)

def U_bath(i_a, bath_k, ACD, thk_bubble):
    U_bath = (i_a/bath_k)*(ACD-thk_bubble)
    return U_bath
#bath_k = bath_k_arkp_eq(T_bath_k=T_bath_k, w_Al2O3=w_Al2O3, w_CaF2=w_CaF2, CR=CR)
bath_k = bath_k_hives_eq(T_bath_k=T_bath_k, w_Al2O3=w_Al2O3, w_AlF3=w_AlF3, w_CaF2=w_CaF2, w_MgF2 = w_MgF2, w_KF=w_KF, w_LiF=w_LiF)
U_bath = U_bath(i_a=i_a, bath_k=bath_k, ACD=ACD, thk_bubble=thk_bubble)

print(f"The bath voltage drop is: {U_bath}")
print(f"The bath conductivity is: {bath_k} S/cm")
print(f"The new anodic surface is: {new_anodic_surface} m2")
print(f"The geometric anodic current density is {i_a}A/cm2")
print(f"The bath voltage drop is: {U_bath}")

