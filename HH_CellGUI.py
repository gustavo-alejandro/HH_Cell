import tkinter as tk
from tkinter import ttk
import math

class Bath:
    def __init__(self):
        # Initialize attribute values
        self.w_Al2O3 = tk.DoubleVar(value=4.2)
        self.w_AlF3 = tk.DoubleVar(value=10.3)
        self.w_CaF2 = tk.DoubleVar(value=7.0)
        self.w_MgF2 = tk.DoubleVar(value=0.3)
        self.w_KF = tk.DoubleVar(value=0.1)
        self.w_LiF = tk.DoubleVar(value=0.0)
        self.bath_temp_K = tk.DoubleVar(value=964 + 273.15)

    def update_attributes(self, w_Al2O3, w_AlF3, w_CaF2, w_MgF2, w_KF, w_LiF, bath_temp_K):
        # Update the attribute values with the new values passed from the GUI
        self.w_Al2O3.set(w_Al2O3)
        self.w_AlF3.set(w_AlF3)
        self.w_CaF2.set(w_CaF2)
        self.w_MgF2.set(w_MgF2)
        self.w_KF.set(w_KF)
        self.w_LiF.set(w_LiF)
        self.bath_temp_K.set(bath_temp_K)

    def bath_conductivity(self):
        """
        Cryolite bath electrical conductivity as function of temperature and chemical composition, assuming only
        species are Al2O3, AlF3, CaF2, MgF2, KF, LiF, each species input in wt%, temperature in K.
        Using electrical conductivity empirical equation from https://doi.org/10.1007/BF02915051
        :return: bath conductivity in 1/ohm
        """
        # Calculate the bath conductivity using the provided equation
        bath_conductivity = math.exp(1.977 - 0.02 * self.w_Al2O3.get() - 0.0131 * self.w_AlF3.get() - 0.006 * self.w_CaF2.get() - 0.0106 * self.w_MgF2.get() - 0.0019 * self.w_KF.get() + 0.0121 * self.w_LiF.get() - 1204.3 / self.bath_temp_K.get())
        return bath_conductivity

    def bath_resistivity(self):
        # Calculate the bath resistivity
        bath_resistivity = 1 / self.bath_conductivity()
        return bath_resistivity

    def Al2O3_solub_A_factor(self):
        # Calculate Al2O3_solub_A_factor using the provided equation
        Al2O3_solub_A_factor = 11.9 - 0.062 * self.w_AlF3.get() - 0.0031 * (self.w_AlF3.get() ** 2) - 0.5 * self.w_LiF.get() - 0.2 * self.w_CaF2.get() - 0.3 * self.w_MgF2.get() + (42 * self.w_LiF.get() * self.w_AlF3.get()) / (2000 + self.w_AlF3.get() * self.w_LiF.get())
        return Al2O3_solub_A_factor

    def Al2O3_solub_B_factor(self):
        # Calculate Al2O3_solub_B_factor using the provided equation
        Al2O3_solub_B_factor = 4.8 - 0.048 * self.w_AlF3.get() + (2.2 * (self.w_LiF.get() ** 1.5)) / (10 + self.w_LiF.get() + 0.001 * self.w_AlF3.get())
        return Al2O3_solub_B_factor

    def Al2O3_sat(self):
        # Calculate Al2O3_sat using the provided equation
        Al2O3_solub_A_factor = self.Al2O3_solub_A_factor()
        Al2O3_solub_B_factor = self.Al2O3_solub_B_factor()
        Al2O3_sat = Al2O3_solub_A_factor * ((self.bath_temp_K.get() - 273.15) / 1000) ** Al2O3_solub_B_factor
        return Al2O3_sat

    def Al2O3_rel_sat(self):
        # Calculate Al2O3_rel_sat using the provided equation
        Al2O3_rel_sat = self.w_Al2O3.get() / self.Al2O3_sat()
        return Al2O3_rel_sat

    def Equil_potential(self):
        """
        This function calculates the equilibrium potential using equation (5) from  https://doi.org/10.1007/978-3-319-48156-2_21

        :return: Equilibium potential in volts
        """
        # Calculate Equil_potential using the provided equation
        bath_temp_K = self.bath_temp_K.get()
        Al2O3_rel_sat = self.Al2O3_rel_sat()
        Equil_potential = 1.897 - 0.00056 * bath_temp_K + (8.314 * bath_temp_K) / (12 * 96485) * math.pow(math.log(1 / Al2O3_rel_sat), 2.77)
        return Equil_potential

    def bath_ratio(self):
        """
        The ratio NaF/AlF3 is called the cryolite ratio and it is 3 in pure cryolite (Na3AlF6)
        Cryolite is dissociated to sodium fluoride and aliminum fluoride Na3AlF6 = 3 NaF + AlF3 https://doi.org/10.1021/j100830a023
        mole ratio (NaF/AlF3) of dissociated cryolite is 3.0
        Molecular weight of sodium fluoride 3*NaF = 3*(22.99g/mol Na + 18.99 g/mol fluoride) = 3*42g/mol
        Molecular weight of Aluminium fluoride AlF3 = 26.98g/mol Al + 3x18.99 g/mol fluoride = 84 g/mol
        Weight ratio 1.5
        Bath composition wt% = %CaF2 + %xAlF3 + %Al2O3 + 3NaF*AlF3
        Equation for bath ratio derived from https://doi.org/10.1007/978-3-319-48156-2_118
        :return:
        """
        # Calculate the bath ratio using the provided equation
        return (1.5 * (100 - self.w_CaF2.get() - self.w_Al2O3.get() - self.w_AlF3.get())) / ((100 - self.w_CaF2.get() - self.w_Al2O3.get()) + (1.5 * self.w_AlF3.get()))


class Anode:
    #initialize attributes
    def __init__(self):
        # Initialize attribute values
        self.length = tk.DoubleVar(value=1600)
        self.width = tk.DoubleVar(value=800)
        self.height = tk.DoubleVar(value=600)

    def bot_surface_area(self):
        self.area = self.length * self.width
        return self.area



class CellGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Aluminium Cell Model")

        # Initialize the bath object
        self.bath = Bath()

        # Load and display the image
        self.image_path = "C:/Users/n11675250/OneDrive - Queensland University of Technology/Aluminium Cell/E/hhprg/cellschema/images/left_riser_gesamt1.png"
        self.load_image()

        self.create_widgets()

    def load_image(self):
        try:
            self.image = tk.PhotoImage(file=self.image_path)
            self.image_label = ttk.Label(self.root, image=self.image)
            self.image_label.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
        except Exception as e:
            print(f"Error loading the image: {e}")

    def create_widgets(self):
        attributes_frame = ttk.LabelFrame(self.root, text="Attributes")
        attributes_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="w")

        attributes_labels = ['w_Al2O3', 'w_AlF3', 'w_CaF2', 'w_MgF2', 'w_KF', 'w_LiF', 'Bath Temperature (K)']
        attributes_vars = [
            self.bath.w_Al2O3, self.bath.w_AlF3, self.bath.w_CaF2,
            self.bath.w_MgF2, self.bath.w_KF, self.bath.w_LiF, self.bath.bath_temp_K
        ]
        slider_ranges = [(0, 10), (0, 10), (0, 10), (0, 10), (0, 10), (0, 10), (1050, 1300)]

        for idx, label in enumerate(attributes_labels):
            ttk.Label(attributes_frame, text=label).grid(row=idx, column=0, padx=5, pady=5)
            slider = ttk.Scale(
                attributes_frame, variable=attributes_vars[idx], from_=slider_ranges[idx][0],
                to=slider_ranges[idx][1], length=50, orient="horizontal"
            )
            slider.grid(row=idx, column=1, padx=5, pady=5)
            slider.set(attributes_vars[idx].get())  # Set the slider value to the initial attribute value
            slider.bind("<ButtonRelease-1>", self.on_slider_release)  # Bind the slider release event
            ttk.Label(attributes_frame, textvariable=attributes_vars[idx]).grid(row=idx, column=2, padx=5, pady=5)

        resistivity_frame = ttk.LabelFrame(self.root, text="Bath Resistivity")
        resistivity_frame.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        self.resistivity_label = ttk.Label(resistivity_frame, text="Bath Resistivity: ")
        self.resistivity_label.grid(row=0, column=0, padx=5, pady=5)

        Equil_potential_frame = ttk.LabelFrame(self.root, text="Equil_potential")
        Equil_potential_frame.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        self.Equil_potential_label = ttk.Label(Equil_potential_frame, text="Equil_potential: ")
        self.Equil_potential_label.grid(row=0, column=0, padx=5, pady=5)

        bath_ratio_frame = ttk.LabelFrame(self.root, text="bath ratio")
        bath_ratio_frame.grid(row=2, column=2, padx=10, pady=10, sticky="w")

        self.bath_ratio_label = ttk.Label(bath_ratio_frame, text="bath_ratio: ")
        self.bath_ratio_label.grid(row=0, column=0, padx=5, pady=5)

        Anode_frame = ttk.LabelFrame(self.root, text="Anode dimensions")
        Anode_frame.grid(row=2, column=3, padx=10, pady=10, sticky="w")

        ttk.Button(self.root, text="Calculate", command=self.update_results).grid(row=3, column=0, columnspan=3, padx=10, pady=10)

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

        # Update the resistivity, Equil_potential, and bath_ratio labels
        self.update_results()

    def update_results(self):
        try:
            resistivity = self.bath.bath_resistivity()
            self.resistivity_label.config(text=f"Bath Resistivity: {resistivity:.4f}")
        except Exception as e:
            print(f"Error calculating bath resistivity: {e}")
            self.resistivity_label.config(text="error")

        try:
            Equil_potential = self.bath.Equil_potential()
            self.Equil_potential_label.config(text=f"Equil_potential: {Equil_potential:.4f}")
        except Exception as e:
            print(f"Error calculating Equil_potential: {e}")
            self.Equil_potential_label.config(text="error")

        try:
            bath_ratio = self.bath.bath_ratio()
            self.bath_ratio_label.config(text=f"bath_ratio: {bath_ratio:.4f}")
        except Exception as e:
            print(f"Error calculating bath_ratio: {e}")
            self.bath_ratio_label.config(text="error")

if __name__ == "__main__":
    root = tk.Tk()
    cell_gui = CellGUI(root)
    root.mainloop()
