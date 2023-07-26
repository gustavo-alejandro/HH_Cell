import tkinter as tk
from tkinter import ttk
import math
#from math import exp, pow, log

class Bath:
    def __init__(self):
        self.attributes = {
            'w_Al2O3': 4.2,
            'w_AlF3': 10.3,
            'w_CaF2': 7,
            'w_MgF2': 0.3,
            'w_KF': 0.1,
            'w_LiF': 0,
            'bath_temp_K': 964 + 273.15
        }

    def bath_conductivity(self):
        w_Al2O3, w_AlF3, w_CaF2, w_MgF2, w_KF, w_LiF, bath_temp_K = self.attributes.values()
        return exp(1.977 - 0.02 * w_Al2O3 - 0.0131 * w_AlF3 - 0.006 * w_CaF2 - 0.0106 * w_MgF2 - 0.0019 * w_KF + 0.0121 * w_LiF - 1204.3 / bath_temp_K)

    def bath_resistivity(self):
        return 1 / self.bath_conductivity()

    def Al2O3_solub_A_factor(self):
        w_AlF3, w_LiF, _CaF2, _MgF2 = self.attributes['w_AlF3'], self.attributes['w_LiF'], self.attributes['w_CaF2'], self.attributes['w_MgF2']
        return 11.9 - 0.062 * w_AlF3 - 0.0031 * pow(w_AlF3, 2) - 0.5 * w_LiF - 0.2 * _CaF2 - 0.3 * _MgF2 + (42 * w_LiF * w_AlF3) / (2000 + w_AlF3 * w_LiF)

    def Al2O3_solub_B_factor(self):
        w_AlF3, w_LiF = self.attributes['w_AlF3'], self.attributes['w_LiF']
        return 4.8 - 0.048 * w_AlF3 + (2.2 * pow(w_LiF, 1.5)) / (10 + w_LiF + 0.001 * w_AlF3)

    def Al2O3_sat(self):
        bath_temp_K = self.attributes['bath_temp_K']
        Al2O3_solub_A = self.Al2O3_solub_A_factor()
        Al2O3_solub_B = self.Al2O3_solub_B_factor()
        return Al2O3_solub_A * pow(((bath_temp_K - 273.15) / 1000), Al2O3_solub_B)

    def Al2O3_rel_sat(self):
        w_Al2O3 = self.attributes['w_Al2O3']
        return w_Al2O3 / self.Al2O3_sat()

    def Equil_potential(self):
        bath_temp_K = self.attributes['bath_temp_K']
        Al2O3_rel_sat = self.Al2O3_rel_sat()
        return 1.897 - 0.00056 * bath_temp_K + (8.314 * bath_temp_K) / (12 * 96485) * pow(math.log(1 / Al2O3_rel_sat), 2.77)

class BathGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Bath Attributes GUI")

        self.bath = Bath()
        self.attributes_labels = list(self.bath.attributes.keys())
        self.slider_ranges = [(0, 10), (0, 10), (0, 10), (0, 10), (0, 10), (0, 10), (1050, 1300)]

        self.attributes_vars = {label: tk.DoubleVar(value=self.bath.attributes[label]) for label in self.attributes_labels}

        self.create_widgets()

    def create_widgets(self):
        image_path = "C:/Users/n11675250/OneDrive - Queensland University of Technology/Aluminium Cell/E/hhprg/cellschema/images/left_riser_gesamt1.png"
        self.load_image(image_path)

        for i, label in enumerate(self.attributes_labels):
            ttk.Label(self.root, text=f"{label}:").grid(row=i, column=0, padx=5, pady=5)
            ttk.Scale(self.root, from_=self.slider_ranges[i][0], to=self.slider_ranges[i][1],
                      variable=self.attributes_vars[label], length=200, orient=tk.HORIZONTAL).grid(row=i, column=1)
            ttk.Label(self.root, textvariable=self.attributes_vars[label]).grid(row=i, column=2, padx=5, pady=5)

        ttk.Button(self.root, text="Reset", command=self.reset_sliders).grid(row=len(self.attributes_labels), column=0,
                                                                             columnspan=3, padx=5, pady=10)

        ttk.Label(self.root, text="bath_conductivity:").grid(row=len(self.attributes_labels) + 1, column=0, padx=5,
                                                             pady=5)
        conductivity_label = ttk.Label(self.root, text="")
        conductivity_label.grid(row=len(self.attributes_labels) + 1, column=1, columnspan=2, padx=5, pady=5)

        ttk.Label(self.root, text="bath_resistivity:").grid(row=len(self.attributes_labels) + 2, column=0, padx=5,
                                                            pady=5)
        resistivity_label = ttk.Label(self.root, text="")
        resistivity_label.grid(row=len(self.attributes_labels) + 2, column=1, columnspan=2, padx=5, pady=5)

        ttk.Label(self.root, text="Al2O3_solub_A_factor:").grid(row=len(self.attributes_labels) + 3, column=0, padx=5,
                                                                 pady=5)
        solub_a_label = ttk.Label(self.root, text="")
        solub_a_label.grid(row=len(self.attributes_labels) + 3, column=1, columnspan=2, padx=5, pady=5)

        ttk.Label(self.root, text="Al2O3_solub_B_factor:").grid(row=len(self.attributes_labels) + 4, column=0, padx=5,
                                                                 pady=5)
        solub_b_label = ttk.Label(self.root, text="")
        solub_b_label.grid(row=len(self.attributes_labels) + 4, column=1, columnspan=2, padx=5, pady=5)

        ttk.Label(self.root, text="Al2O3_sat:").grid(row=len(self.attributes_labels) + 5, column=0, padx=5, pady=5)
        sat_label = ttk.Label(self.root, text="")
        sat_label.grid(row=len(self.attributes_labels) + 5, column=1, columnspan=2, padx=5, pady=5)

        ttk.Label(self.root, text="Al2O3_rel_sat:").grid(row=len(self.attributes_labels) + 6, column=0, padx=5, pady=5)
        rel_sat_label = ttk.Label(self.root, text="")
        rel_sat_label.grid(row=len(self.attributes_labels) + 6, column=1, columnspan=2, padx=5, pady=5)

        ttk.Label(self.root, text="Equil_potential:").grid(row=len(self.attributes_labels) + 7, column=0, padx=5,
                                                           pady=5)
        equil_potential_label = ttk.Label(self.root, text="")
        equil_potential_label.grid(row=len(self.attributes_labels) + 7, column=1, columnspan=2, padx=5, pady=5)

        ttk.Button(self.root, text="Calculate", command=lambda: self.calculate_values(conductivity_label,
                                                                                     resistivity_label,
                                                                                     solub_a_label,
                                                                                     solub_b_label,
                                                                                     sat_label,
                                                                                     rel_sat_label,
                                                                                     equil_potential_label)).grid(
            row=len(self.attributes_labels) + 8, column=0, columnspan=3, padx=5, pady=10)

    def load_image(self, image_path):
        try:
            image = tk.PhotoImage(file=image_path)
            image_label = ttk.Label(self.root, image=image)
            image_label.image = image
            image_label.grid(row=0, column=3, rowspan=len(self.attributes_labels) + 8, padx=5, pady=5)
        except tk.TclError:
            print(f"Failed to load image from {image_path}")

    def calculate_values(self, conductivity_label, resistivity_label, solub_a_label, solub_b_label, sat_label,
                         rel_sat_label, equil_potential_label):
        for label in self.attributes_labels:
            self.bath.attributes[label] = self.attributes_vars[label].get()

        conductivity = self.bath.bath_conductivity()
        resistivity = self.bath.bath_resistivity()
        solub_a = self.bath.Al2O3_solub_A_factor()
        solub_b = self.bath.Al2O3_solub_B_factor()
        sat = self.bath.Al2O3_sat()
        rel_sat = self.bath.Al2O3_rel_sat()
        equil_potential = self.bath.Equil_potential()

        conductivity_label.config(text=f"{conductivity:.4f}")
        resistivity_label.config(text=f"{resistivity:.4f}")
        solub_a_label.config(text=f"{solub_a:.4f}")
        solub_b_label.config(text=f"{solub_b:.4f}")
        sat_label.config(text=f"{sat:.4f}")
        rel_sat_label.config(text=f"{rel_sat:.4f}")
        equil_potential_label.config(text=f"{equil_potential:.4f}")

    def reset_sliders(self):
        for label in self.attributes_labels:
            self.attributes_vars[label].set(self.bath.attributes[label])


if __name__ == "__main__":
    root = tk.Tk()
    bath_gui = BathGUI(root)
    root.mainloop()
