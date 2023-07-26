import tkinter as tk
from tkinter import ttk
import math

class BathGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Aluminium Cell Model")

        # Initialize attribute values
        self.w_Al2O3 = tk.DoubleVar(value=4.2)
        self.w_AlF3 = tk.DoubleVar(value=10.3)
        self.w_CaF2 = tk.DoubleVar(value=7.0)
        self.w_MgF2 = tk.DoubleVar(value=0.3)
        self.w_KF = tk.DoubleVar(value=0.1)
        self.w_LiF = tk.DoubleVar(value=0.0)
        self.bath_temp_K = tk.DoubleVar(value=964 + 273.15)

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

    def bath_conductivity(self):
        w_Al2O3 = self.w_Al2O3.get()
        w_AlF3 = self.w_AlF3.get()
        w_CaF2 = self.w_CaF2.get()
        w_MgF2 = self.w_MgF2.get()
        w_KF = self.w_KF.get()
        w_LiF = self.w_LiF.get()
        temperature = self.bath_temp_K.get()

        # Calculate the bath conductivity using the provided equation
        bath_conductivity = math.exp(1.977 - 0.02 * w_Al2O3 - 0.0131 * w_AlF3 - 0.006 * w_CaF2 - 0.0106 * w_MgF2 - 0.0019 * w_KF + 0.0121 * w_LiF - 1204.3 / temperature)
        return bath_conductivity

    def bath_resistivity(self):
        bath_conductivity = self.bath_conductivity()

        # Calculate the bath resistivity
        bath_resistivity = 1 / bath_conductivity
        return bath_resistivity

    def Al2O3_solub_A_factor(self):
        w_AlF3 = self.w_AlF3.get()
        w_LiF = self.w_LiF.get()
        w_CaF2 = self.w_CaF2.get()
        w_MgF2 = self.w_MgF2.get()

        # Calculate Al2O3_solub_A_factor using the provided equation
        Al2O3_solub_A_factor = 11.9 - 0.062 * w_AlF3 - 0.0031 * (w_AlF3 ** 2) - 0.5 * w_LiF - 0.2 * w_CaF2 - 0.3 * w_MgF2 + (42 * w_LiF * w_AlF3) / (2000 + w_AlF3 * w_LiF)
        return Al2O3_solub_A_factor

    def Al2O3_solub_B_factor(self):
        w_AlF3 = self.w_AlF3.get()
        w_LiF = self.w_LiF.get()

        # Calculate Al2O3_solub_B_factor using the provided equation
        Al2O3_solub_B_factor = 4.8 - 0.048 * w_AlF3 + (2.2 * (w_LiF ** 1.5)) / (10 + w_LiF + 0.001 * w_AlF3)
        return Al2O3_solub_B_factor

    def Al2O3_sat(self):
        Al2O3_solub_A_factor = self.Al2O3_solub_A_factor()
        Al2O3_solub_B_factor = self.Al2O3_solub_B_factor()
        bath_temp_K = self.bath_temp_K.get()

        # Calculate Al2O3_sat using the provided equation
        Al2O3_sat = Al2O3_solub_A_factor * ((bath_temp_K - 273.15) / 1000) ** Al2O3_solub_B_factor
        return Al2O3_sat

    def Al2O3_rel_sat(self):
        w_Al2O3 = self.w_Al2O3.get()
        Al2O3_sat = self.Al2O3_sat()

        # Calculate Al2O3_rel_sat using the provided equation
        Al2O3_rel_sat = w_Al2O3 / Al2O3_sat
        return Al2O3_rel_sat

    def Equil_potential(self):
        bath_temp_K = self.bath_temp_K.get()
        Al2O3_rel_sat = self.Al2O3_rel_sat()

        # Calculate Equil_potential using the provided equation
        Equil_potential = 1.897 - 0.00056 * bath_temp_K + (8.314 * bath_temp_K) / (12 * 96485) * math.pow(math.log(1 / Al2O3_rel_sat), 2.77)
        return Equil_potential

    def bath_ratio(self):
        return (1.5 * (100 - self.w_CaF2.get() - self.w_Al2O3.get() - self.w_AlF3.get())) / (
                (100 - self.w_CaF2.get() - self.w_Al2O3.get()) + (1.5 * self.w_AlF3.get()))

    def create_widgets(self):
        attributes_frame = ttk.LabelFrame(self.root, text="Attributes")
        attributes_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="w")

        attributes_labels = ['w_Al2O3', 'w_AlF3', 'w_CaF2', 'w_MgF2', 'w_KF', 'w_LiF', 'Bath Temperature (K)']
        attributes_vars = [self.w_Al2O3, self.w_AlF3, self.w_CaF2, self.w_MgF2, self.w_KF, self.w_LiF, self.bath_temp_K]

        slider_ranges = [(0, 10), (0, 10), (0, 10), (0, 10), (0, 10), (0, 10), (1050, 1300)]

        for idx, label in enumerate(attributes_labels):
            ttk.Label(attributes_frame, text=label).grid(row=idx, column=0, padx=5, pady=5)
            ttk.Scale(attributes_frame, variable=attributes_vars[idx], from_=slider_ranges[idx][0], to=slider_ranges[idx][1], length=50, orient="horizontal").grid(row=idx, column=1, padx=5, pady=5)
            ttk.Label(attributes_frame, textvariable=attributes_vars[idx]).grid(row=idx, column=2, padx=5, pady=5)

        # Display boxes for bath conductivity, bath resistivity, Al2O3_solub_A_factor, Al2O3_solub_B_factor, Al2O3_sat, Al2O3_rel_sat, and Equil_potential
        conductivity_frame = ttk.LabelFrame(self.root, text="Bath Conductivity")
        conductivity_frame.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        self.conductivity_label = ttk.Label(conductivity_frame, text="Bath Conductivity: ")
        self.conductivity_label.grid(row=0, column=0, padx=5, pady=5)

        resistivity_frame = ttk.LabelFrame(self.root, text="Bath Resistivity")
        resistivity_frame.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        self.resistivity_label = ttk.Label(resistivity_frame, text="Bath Resistivity: ")
        self.resistivity_label.grid(row=0, column=0, padx=5, pady=5)

        solub_A_frame = ttk.LabelFrame(self.root, text="Al2O3_solub_A_factor")
        solub_A_frame.grid(row=2, column=2, padx=10, pady=10, sticky="w")

        self.solub_A_label = ttk.Label(solub_A_frame, text="Al2O3_solub_A_factor: ")
        self.solub_A_label.grid(row=0, column=0, padx=5, pady=5)

        solub_B_frame = ttk.LabelFrame(self.root, text="Al2O3_solub_B_factor")
        solub_B_frame.grid(row=3, column=0, padx=10, pady=10, sticky="w")

        self.solub_B_label = ttk.Label(solub_B_frame, text="Al2O3_solub_B_factor: ")
        self.solub_B_label.grid(row=0, column=0, padx=5, pady=5)

        Al2O3_sat_frame = ttk.LabelFrame(self.root, text="Al2O3_sat")
        Al2O3_sat_frame.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        self.Al2O3_sat_label = ttk.Label(Al2O3_sat_frame, text="Al2O3_sat: ")
        self.Al2O3_sat_label.grid(row=0, column=0, padx=5, pady=5)

        Al2O3_rel_sat_frame = ttk.LabelFrame(self.root, text="Al2O3_rel_sat")
        Al2O3_rel_sat_frame.grid(row=3, column=2, padx=10, pady=10, sticky="w")

        self.Al2O3_rel_sat_label = ttk.Label(Al2O3_rel_sat_frame, text="Al2O3_rel_sat: ")
        self.Al2O3_rel_sat_label.grid(row=0, column=0, padx=5, pady=5)

        Equil_potential_frame = ttk.LabelFrame(self.root, text="Equil_potential")
        Equil_potential_frame.grid(row=4, column=0, padx=10, pady=10, sticky="w")

        self.Equil_potential_label = ttk.Label(Equil_potential_frame, text="Equil_potential: ")
        self.Equil_potential_label.grid(row=0, column=0, padx=5, pady=5)

        #ttk.Button(self.root, text="Calculate", command=self.update_results).grid(row=5, column=0, columnspan=3, padx=10, pady=10)

        bath_ratio_frame = ttk.LabelFrame(self.root, text="bath ratio")
        bath_ratio_frame.grid(row=4, column=1, padx=10, pady=10, sticky="w")

        self.bath_ratio_label = ttk.Label(bath_ratio_frame, text="bath_ratio: ")
        self.bath_ratio_label.grid(row=0, column=0, padx=5, pady=5)

        ttk.Button(self.root, text="Calculate", command=self.update_results).grid(row=4, column=3, columnspan=3,
                                                                                  padx=10, pady=10)

    def update_results(self):
        conductivity = self.bath_conductivity()
        resistivity = self.bath_resistivity()
        solub_A = self.Al2O3_solub_A_factor()
        solub_B = self.Al2O3_solub_B_factor()
        Al2O3_sat = self.Al2O3_sat()
        Al2O3_rel_sat = self.Al2O3_rel_sat()
        Equil_potential = self.Equil_potential()
        bath_ratio = self.bath_ratio()

        self.conductivity_label.config(text=f"Bath Conductivity: {conductivity:.4f}")
        self.resistivity_label.config(text=f"Bath Resistivity: {resistivity:.4f}")
        self.solub_A_label.config(text=f"Al2O3_solub_A_factor: {solub_A:.4f}")
        self.solub_B_label.config(text=f"Al2O3_solub_B_factor: {solub_B:.4f}")
        self.Al2O3_sat_label.config(text=f"Al2O3_sat: {Al2O3_sat:.4f}")
        self.Al2O3_rel_sat_label.config(text=f"Al2O3_rel_sat: {Al2O3_rel_sat:.4f}")
        self.Equil_potential_label.config(text=f"Equil_potential: {Equil_potential:.4f}")
        self.bath_ratio_label.config(text=f"bath_ratio: {bath_ratio:.4f}")

if __name__ == "__main__":
    root = tk.Tk()
    bath_gui = BathGUI(root)
    root.mainloop()
