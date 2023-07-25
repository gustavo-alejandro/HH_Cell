from HH_Cell_Classes import *
#Cell input
cell_current = 360000

#Cell objects
bath = Bath()
anode_assy = Anode_assy()

#Bath methods, conductivity calc

v_drop = anode_assy.voltage_drop(cell_current=cell_current)
anode_surface = anode_assy.anode_block_surface()

#Change bath composition
bath.composition['w_Al2O3'] = [4.2]
bath.composition['w_AlF3'] = [10.3]
bath.composition['w_MgF2'] = [0.3]
bath.composition['w_CaF2'] = [7]

bath_k = bath.bath_k_hives_eq(T_bath_k=964+273.15)

br = bath.bath_ratio()
cr = bath.cryolite_ratio()
ir = bath.rx_limit_current_dens()
id = anode_assy.anode_current_dens(current=cell_current)
surf_pol = 1.142e-5 * math.log(anode_assy.anode_block['anode bake temp'].item()) * bath.temperature * math.log(id/ir)
print(bath_k)
