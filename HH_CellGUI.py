from HH_Cell_Model_Classes import *
import tkinter as tk
from tkinter import ttk
class CellGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Aluminium Cell Model")

        # Initialize the bath object and anode object
        self.bath = Bath()
        self.anode = Anode()
        self.anode_assembly = Anode_assembly()
        self.cell = Cell_input()

        # Load and display the image
        self.image_path = "C:/Users/n11675250/OneDrive - Queensland University of Technology/Aluminium Cell/E/hhprg/cellschema/images/left_riser_gesamt1.png"
        self.load_image()

        self.create_widgets()

    def load_image(self):
        try:
            self.image = tk.PhotoImage(file=self.image_path)
            self.image = self.image.subsample(2,2)
            self.image_label = ttk.Label(self.root, image=self.image, width=100)
            self.image_label.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
        except Exception as e:
            print(f"Error loading the image: {e}")

    def create_widgets(self):
        attributes_frame = ttk.LabelFrame(self.root, text="Bath comp wt%")
        attributes_frame.grid(row=0, column=5, columnspan=1, padx=5, pady=5, sticky="nw")

        attributes_labels = ['w_Al2O3', 'w_AlF3', 'w_CaF2', 'w_MgF2', 'w_KF', 'w_LiF', 'Bath Temperature (K)']
        attributes_vars = [
            self.bath.w_Al2O3, self.bath.w_AlF3, self.bath.w_CaF2,
            self.bath.w_MgF2, self.bath.w_KF, self.bath.w_LiF, self.bath.bath_temp_K
        ]
        slider_ranges = [(0, 11), (0, 11), (0, 11), (0, 11), (0, 11), (0, 11), (1050, 1400)]

        for idx, label in enumerate(attributes_labels):
            ttk.Label(attributes_frame, text=label, width=10).grid(row=idx, column=0, padx=5, pady=5)
            slider = ttk.Scale(
                attributes_frame, variable=attributes_vars[idx], from_=slider_ranges[idx][0],
                to=slider_ranges[idx][1], length=50, orient="horizontal"
            )
            slider.grid(row=idx, column=1, padx=5, pady=5)
            slider.set(attributes_vars[idx].get())  # Set the slider value to the initial attribute value
            slider.bind("<ButtonRelease-1>", self.on_slider_release)  # Bind the slider release event
            ttk.Label(attributes_frame, textvariable=attributes_vars[idx], width=4).grid(row=idx, column=2, padx=5, pady=5)

        resistivity_frame = ttk.LabelFrame(self.root, text="Bath Resistivity")
        resistivity_frame.grid(row=4, column=5, padx=10, pady=10, sticky="w")

        self.resistivity_label = ttk.Label(resistivity_frame, text="Bath Resistivity: ")
        self.resistivity_label.grid(row=0, column=0, padx=5, pady=5)

        Equil_potential_frame = ttk.LabelFrame(self.root, text="Equil_potential")
        Equil_potential_frame.grid(row=1, column=5, padx=10, pady=10, sticky="nw")

        self.Equil_potential_label = ttk.Label(Equil_potential_frame, text="Equil_potential: ")
        self.Equil_potential_label.grid(row=3, column=5, padx=5, pady=5)

        bath_ratio_frame = ttk.LabelFrame(self.root, text="bath ratio")
        bath_ratio_frame.grid(row=2, column=5, padx=10, pady=10, sticky="nw")

        self.bath_ratio_label = ttk.Label(bath_ratio_frame, text="bath_ratio: ")
        self.bath_ratio_label.grid(row=0, column=0, padx=5, pady=5)

        rx_current_limit_frame = ttk.LabelFrame(self.root, text="rx current limit")
        rx_current_limit_frame.grid(row=3, column=5, padx=10, pady=10, sticky="nw")

        self.rx_current_limit_label = ttk.Label(rx_current_limit_frame, text="rx current limit: ")
        self.rx_current_limit_label.grid(row=0, column=0, padx=5, pady=5)

        # Anode attributes input GUI

        anode_frame = ttk.LabelFrame(self.root, text="Anode data")
        anode_frame.grid(row=0, column=6, padx=5, pady=10, sticky="nw")

        ttk.Label(anode_frame, text="Length new", width=12).grid(row=0, column=0, padx=5, pady=5)
        length_new_entry = ttk.Entry(anode_frame, textvariable=self.anode.length_new, width=5)
        length_new_entry.grid(row=0, column=1, padx=1, pady=1)

        ttk.Label(anode_frame, text="Length spent", width=12).grid(row=1, column=0, padx=5, pady=5)
        length_old_entry = ttk.Entry(anode_frame, textvariable=self.anode.length_spent, width=5)
        length_old_entry.grid(row=1, column=1, padx=1, pady=1)

        ttk.Label(anode_frame, text="Width new", width=12).grid(row=2, column=0, padx=5, pady=5)
        width_new_entry = ttk.Entry(anode_frame, textvariable=self.anode.width_new, width=5)
        width_new_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(anode_frame, text="Width spent", width=12).grid(row=3, column=0, padx=5, pady=5)
        width_old_entry = ttk.Entry(anode_frame, textvariable=self.anode.width_spent, width=5)
        width_old_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(anode_frame, text="Height", width=6).grid(row=4, column=0, padx=5, pady=5)
        height_entry = ttk.Entry(anode_frame, textvariable=self.anode.height, width=5)
        height_entry.grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(anode_frame, text="Age", width=6).grid(row=5, column=0, padx=5, pady=5)
        age_entry = ttk.Entry(anode_frame, textvariable=self.anode.age, width=5)
        age_entry.grid(row=5, column=1, padx=5, pady=5)

        ttk.Label(anode_frame, text="n anodes", width=6).grid(row=6, column=0, padx=5, pady=5)
        n_anodes_entry = ttk.Entry(anode_frame, textvariable=self.anode.n_anodes, width=5)
        n_anodes_entry.grid(row=6, column=1, padx=5, pady=5)

        ttk.Label(anode_frame, text="Depth subm", width=6).grid(row=7, column=0, padx=5, pady=5)
        depth_imm_entry = ttk.Entry(anode_frame, textvariable=self.anode.depth_immers, width=5)
        depth_imm_entry.grid(row=7, column=1, padx=5, pady=5)

        ttk.Label(anode_frame, text="bake temp", width=6).grid(row=8, column=0, padx=5, pady=5)
        bake_temp_entry = ttk.Entry(anode_frame, textvariable=self.anode.bake_temp, width=5)
        bake_temp_entry.grid(row=8, column=1, padx=5, pady=5)

        # Anode spacing input GUI

        anode_frame = ttk.LabelFrame(self.root, text="Anode spacing")
        anode_frame.grid(row=0, column=7, padx=5, pady=10, sticky="nw")

        ttk.Label(anode_frame, text="S_1", width=12).grid(row=0, column=0, padx=5, pady=5)
        length_new_entry = ttk.Entry(anode_frame, textvariable=self.anode.S_1, width=5)
        length_new_entry.grid(row=0, column=1, padx=1, pady=1)

        ttk.Label(anode_frame, text="S_2", width=12).grid(row=1, column=0, padx=5, pady=5)
        length_new_entry = ttk.Entry(anode_frame, textvariable=self.anode.S_2, width=5)
        length_new_entry.grid(row=1, column=1, padx=1, pady=1)

        ttk.Label(anode_frame, text="S_3", width=12).grid(row=2, column=0, padx=5, pady=5)
        length_new_entry = ttk.Entry(anode_frame, textvariable=self.anode.S_3, width=5)
        length_new_entry.grid(row=2, column=1, padx=1, pady=1)

        ttk.Label(anode_frame, text="S_4", width=12).grid(row=3, column=0, padx=5, pady=5)
        length_new_entry = ttk.Entry(anode_frame, textvariable=self.anode.S_4, width=5)
        length_new_entry.grid(row=3, column=1, padx=1, pady=1)


        #Anode calculations output frame GUI

        anode_calc_frame = ttk.LabelFrame(self.root, text="anode calc")
        anode_calc_frame.grid(row=1, column=6, padx=5, pady=5, sticky="nw")

        self.bath_eff_area_field_gui = ttk.Label(anode_calc_frame, text="Bath eff area:     cm2")
        self.bath_eff_area_field_gui.grid(row=0, column=0, padx=5, pady=5, sticky="nw")

        self.current_density_field_gui = ttk.Label(anode_calc_frame, text="Current density:    A/cm2")
        self.current_density_field_gui.grid(row=1, column=0, padx=5, pady=5, sticky="nw")

        self.critical_current_density_field_gui = ttk.Label(anode_calc_frame, text="Critical current density:    A/cm2")
        self.critical_current_density_field_gui.grid(row=2, column=0, padx=5, pady=5, sticky="nw")

        self.surface_overvolt_field_gui = ttk.Label(anode_calc_frame, text="surf overvolt:    V")
        self.surface_overvolt_field_gui.grid(row=3, column=0, padx=5, pady=5, sticky="nw")

        self.concentration_overvolt_field_gui = ttk.Label(anode_calc_frame, text="conc overvolt:    V")
        self.concentration_overvolt_field_gui.grid(row=4, column=0, padx=5, pady=5, sticky="nw")

        #Cell input frame GUI

        cell_frame = ttk.LabelFrame(self.root, text="Cell input data")
        cell_frame.grid(row=1, column=0, padx=5, pady=10, sticky="nw")

        ttk.Label(cell_frame, text="Current", width=10).grid(row=0, column=0, padx=5, pady=5)
        cell_current_entry = ttk.Entry(cell_frame, textvariable=self.cell.current, width=6)
        cell_current_entry.grid(row=0, column=1, padx=1, pady=1)

        ttk.Label(cell_frame, text="ACD", width=10).grid(row=1, column=0, padx=5, pady=5)
        ACD_entry = ttk.Entry(cell_frame, textvariable=self.cell.ACD, width=6)
        ACD_entry.grid(row=1, column=1, padx=1, pady=1)

        ttk.Button(self.root, text="Calculate", command=self.update_results).grid(row=5, column=0, columnspan=3, padx=10, pady=10)

        # Components of cell voltage

        volt_table = ttk.LabelFrame(self.root, text="Components of cell voltage")
        volt_table.grid(row=0, column=8, padx=5, pady=10, sticky="nw")

        self.volt_table_field_Eq_pot_gui = ttk.Label(volt_table, text="Equilibrium potential:     V")
        self.volt_table_field_Eq_pot_gui.grid(row=0, column=0, padx=5, pady=5, sticky="nw")

        self.volt_table_surf_overvolt_gui = ttk.Label(volt_table, text="Surf overvolt:     V")
        self.volt_table_surf_overvolt_gui.grid(row=1, column=0, padx=5, pady=5, sticky="nw")

        self.volt_table_conc_overvolt_gui = ttk.Label(volt_table, text="Conc overvolt:     V")
        self.volt_table_conc_overvolt_gui.grid(row=2, column=0, padx=5, pady=5, sticky="nw")

    def on_slider_release(self, event):
        # Update the bath attributes with the new values from the sliders
        self.bath.update_attributes(
            self.bath.w_Al2O3.get(),
            self.bath.w_AlF3.get(),
            self.bath.w_CaF2.get(),
            self.bath.w_MgF2.get(),
            self.bath.w_KF.get(),
            self.bath.w_LiF.get(),
            self.bath.bath_temp_K.get()
        )

    def update_results(self):
        # Rest of the code remains unchanged
        try:
            self.anode.update_attributes(
                self.anode.length_new.get(),
                self.anode.width_new.get(),
                self.anode.height.get(),
                self.anode.depth_immers.get(),
                self.anode.n_anodes.get()
            )
        except:
            print("error updating anode")

        try:
            resistivity = self.bath.bath_resistivity()
            self.resistivity_label.config(text=f"Bath Resistivity: {resistivity:.4f}")
        except Exception as e:
            print(f"Error calculating bath resistivity: {e}")
            self.resistivity_label.config(text="error")

        try:
            Equil_potential = self.bath.Equil_potential()
            self.Equil_potential_label.config(text=f"Equil_potential: {Equil_potential:.4f}")
            self.volt_table_field_Eq_pot_gui.config(text=f"Equil_potential: {Equil_potential:.4f}")
        except Exception as e:
            print(f"Error calculating Equil_potential: {e}")
            self.Equil_potential_label.config(text="error")

        try:
            bath_ratio = self.bath.bath_ratio()
            self.bath_ratio_label.config(text=f"bath_ratio: {bath_ratio:.4f}")
        except Exception as e:
            print(f"Error calculating bath_ratio: {e}")
            self.bath_ratio_label.config(text="error")

        try:
            n_anodes = self.anode.n_anodes.get()
            ACD = self.cell.ACD.get()
            current = self.cell.current.get()
            T_bath_K=self.bath.bath_temp_K.get()
            rx_current_limit = self.bath.rx_limited_current_density()
            surface_overvolt = self.anode.surface_overvoltage(current, n_anodes, ACD,T_bath_K, rx_current_limit)
            self.rx_current_limit_label.config(text=f"rx limit: {rx_current_limit:.4f}")
            self.volt_table_surf_overvolt_gui.config(text=f"Surface overvolt: {surface_overvolt:.4f}")
            self.surface_overvolt_field_gui.config(text=f"Surf overvolt: {surface_overvolt:.2f} V")
        except Exception as e:
            print(f"Error calculating rx current limit: {e}")
            self.rx_current_limit_label.config(text="error")

        try:

            n_anodes = self.anode.n_anodes.get()
            ACD = self.cell.ACD.get()
            bot_anode_surface = self.anode.bath_eff_area(ACD)
            self.bath_eff_area_field_gui.config(text=f"Bath eff area: {bot_anode_surface:.2f} cm2")
            current = self.cell.current.get()
            T_b_K = self.bath.bath_temp_K.get()
            length = self.anode.length_new.get()
            width = self.anode.width_new.get()
            w_Al2O3 = self.bath.w_Al2O3.get()
            current_intensity = self.anode.current_intensity(current, n_anodes, ACD)
            critical_current_intensity = self.anode.concentration_limit_current_density(n_anodes, length, width, T_b_K, w_Al2O3)
            anode_assy_v_drop = self.anode_assembly.voltage_drop(current)
            print(anode_assy_v_drop)
            #surface_overvolt = self.anode.surface_overvoltage(current, n_anodes, ACD)
            conc_overvolt = self.anode.concentration_overvolt(current, n_anodes, ACD, length, width, T_b_K, w_Al2O3)
            self.current_density_field_gui.config(text=f"Current density: {current_intensity:.2f} A/cm2")
            #self.surface_overvolt_field_gui.config(text=f"Surf overvolt: {surface_overvolt:.2f} V")
            self.concentration_overvolt_field_gui.config(text=f"Conc overvolt: {conc_overvolt:.2f} V")
            self.critical_current_density_field_gui.config(text=f"Critical current density: {critical_current_intensity:.2f} A/cm2")
            #self.volt_table_field_Eq_pot_gui.config(text=f"Equil_potential: {Equil_potential:.4f}")
            #self.volt_table_surf_overvolt_gui.config(text=f"Surface overvolt: {surface_overvolt:.4f}")
            self.volt_table_conc_overvolt_gui.config(text=f"Conc overvolt: {conc_overvolt:.4f}")
        except Exception as e:
            print(f"Error calculating anode attributes: {e}")
            self.bath_eff_area_field_gui.config(text="error")
            #self.current_intensity_label.config(text="error")
        try:
            print(f"Resistance table anode assembly:")
            print(self.anode_assembly.resistance)
        except:
            print("Error anode assy")

if __name__ == "__main__":
    root = tk.Tk()
    print(f"Faraday: {F}")

    cell_gui = CellGUI(root)
    root.mainloop()
