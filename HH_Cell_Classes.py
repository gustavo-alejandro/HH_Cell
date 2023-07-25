import math
import pandas as pd
class Bath:#Blueprint for bath
    #Attributes
    def __init__(self, w_Al2O3=2.5, w_AlF3=11, w_CaF2=4.5, w_MgF2=0.3, w_KF=0.1, w_LiF=0.5):
        self.composition = pd.DataFrame(
            {'w_Al2O3': [2.5], 'w_AlF3': [11], 'w_CaF2': [4.5], 'w_MgF2': [0.3],
             'w_KF': [0.1], 'w_LiF': [0]})
        self.temperature = 960 + 273.15


    def bath_k_ckv_eq(self, T_bath_c):  # bath conductivity Chrenkova et. eal eq. Density, Electrical Conductivity And VIscosity Of Low Melting Baths For Aluminum Electrolysis
        self.bath_k = -7.332 + 1.742e-2 * T_bath_c - 7.313e-6 * pow(T_bath_c, 2) - 1.866e-4 * pow(self.w_AlF3,
                                                                                             2) - 2.824e-5 * self.w_AlF3 * T_bath_c + \
                 4.613e-2 * self.w_LiF + 2.046e-4 * pow(self.w_LiF,
                                                   2) - 4.695e-5 * self.w_Al2O3 * T_bath_c + 2.462e-4 * self.w_AlF3 * self.w_LiF + 2.003e-3 * self.w_AlF3 * self.w_Al2O3 - \
                 5.546e-5 * self.w_AlF3 * self.w_LiF * self.w_Al2O3
        return self.bath_k

    def bath_k_arkp_eq(self, T_bath_k, w_Al2O3, w_CaF2, CR):
        bath_k = -1.87 + 3.23e-3 * T_bath_k - 2.99e-2 * self.w_Al2O3 + 4.70e-1 * CR - 4.37e-2 * self.w_CaF2
        return self.bath_k

    def bath_k_hives_eq(self, T_bath_k):  # Hives eq https://doi.org/10.1007/BF02915051
        self.bath_k = math.exp(
            1.977 - 0.02 * self.composition['w_Al2O3'].item() - 0.0131 * self.composition['w_AlF3'].item() - 0.006 * self.composition['w_CaF2'].item() - 0.0106 * self.composition['w_MgF2'].item() - 0.0019 * self.composition['w_KF'].item() + 0.0121 * self.composition['w_LiF'].item() - 1204.3 / T_bath_k)
        return self.bath_k
    def bath_ratio(self):
        self.br = (1.5 * (100 - self.composition['w_CaF2'].item() - self.composition['w_Al2O3'].item() - self.composition[
            'w_AlF3'].item())) / ((100 - self.composition['w_CaF2'].item() - self.composition['w_Al2O3'].item()) + (
                    1.5 * self.composition['w_AlF3'].item()))
        return self.br
    def cryolite_ratio(self):
        self.bath_ratio()
        self.cr = self.br*2
        return self.cr
    def rx_limit_current_dens(self):
        self.cryolite_ratio()
        self.rx_limit_current_dens = math.exp(
            0.56 * math.log(self.composition['w_Al2O3'].item() + self.composition['w_LiF'].item() / 4) + 0.276 *
            (self.cr - 1.5) - 5.849)
        return self.rx_limit_current_dens


class Anode_assy:
    def __init__(self):
        self.resistance = pd.DataFrame(
            {'riser': [8.1978e-8], 'flexibles': [8.1978e-8], 'anode bridge': [0], 'clamp': [4.28571e-8],
             'anode rod': [3.95556e-8], 'yoke': [1.01087e-7], 'thimble': [0], 'anode block': [5.36087e-7]})#resistance values in ohm
        self.data = pd.DataFrame({'age': [0], 'number anodes': [32]})
        self.anode_block = pd.DataFrame({'anode length': [1.45], 'anode width': [0.54], 'anode height': [0.6],
                                         'anode age': [0], 'anode bake temp': [1100+273.15]})

    def voltage_drop(self, cell_current):
        self.v_drop = self.resistance.mul(cell_current)
        return self.v_drop
    def anode_block_surface(self):
        self.surface = self.anode_block['anode length'].item()*self.anode_block['anode width'].item()*self.data['number anodes'].item()
        return self.surface
    def anode_current_dens(self, current):
        self.i_cd = current / (self.surface*self.data['number anodes'].item())
        return self.i_cd

    def anode_surface_polariz(self, current):
        bath = Bath()
        Bath.bath_ratio(self)
        Bath.cryolite_ratio(self)
        rx_limit_current_dens = Bath.rx_limit_current_dens(self)
        self.surf_pol = 1.142e-5 * math.log(self.anode_block['anode bake temp'].item()) * self.Bath.temperature * math.log(self.i_cd/rx_limit_current_dens)
