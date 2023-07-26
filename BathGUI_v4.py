import tkinter as tk
from tkinter import ttk
from math import exp, pow, log

class Bath:
    def __init__(self, w_Al2O3=4.2, w_AlF3=10.3, w_CaF2=7, w_MgF2=0.3, w_KF=0.1, w_LiF=0, bath_temp_K=964+273.15):
        self.w_Al2O3 = w_Al2O3
        self.w_AlF3 = w_AlF3
        self.w_CaF2 = w_CaF2
        self.w_MgF2 = w_MgF2
        self.w_KF = w_KF
        self.w_LiF = w_LiF
        self.bath_temp_K = bath_temp_K

    def bath_conductivity(self):
        temperature = self.bath_temp_K
        return exp(1.977 - 0.02 * self.w_Al2O3 - 0.0131 * self.w_AlF3 - 0.006 * self.w_CaF2
                   - 0.0106 * self.w_MgF2 - 0.0019 * self.w_KF + 0.0121 * self.w_LiF - 1204.3 / temperature)

    def bath_resistivity(self):
        return 1 / self.bath_conductivity()

    def Al2O3_solub_A_factor(self):
        return 11.9 - 0.062 * self.w_AlF3 - 0.0031 * pow(self.w_AlF3, 2) - 0.5 * self.w_LiF - 0.2 * self.w_CaF2 \
               - 0.3 * self.w_MgF2 + (42 * self.w_LiF * self.w_AlF3) / (2000 + self.w_AlF3 * self.w_LiF)

    def Al2O3_solub_B_factor(self):
        return 4.8 - 0.048 * self.w_AlF3 + (2.2 * pow(self.w_LiF, 1.5)) / (10 + self.w_LiF + 0.001 * self.w_AlF3)

    def Al2O3_sat(self):
        return self.Al2O3_solub_A_factor() * pow(((self.bath_temp_K - 273.15) / 1000), self.Al2O3_solub_B_factor())

    def Al2O3_rel_sat(self):
        return self.w_Al2O3 / self.Al2O3_sat()

    def Equil_potential(self):
        return 1.897 - 0.00056 * self.bath_temp_K + (8.314 * self.bath_temp_K) / (12 * 96485) * pow(
            log(1 / self.Al2O3_rel_sat()), 2.77)

class BathGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Bath Properties GUI")
        self.bath = Bath()

        self.image_path = r"C:\Users\n11675250\OneDrive - Queensland University of Technology\Aluminium Cell\E\hhprg\cellschema\images\left_riser_gesamt1.png"
        self.image = tk.PhotoImage(file=self.image_path)
        self.label_image = tk.Label(root, image=self.image)
        self.label_image.grid(row=0, column=0, columnspan=4)

        self.attributes = ["w_Al2O3", "w_AlF3", "w_CaF2", "w_MgF2", "w_KF", "w_LiF", "bath_temp_K"]
        self.initial_values = {"w_Al2O3": 4.2, "w_AlF3": 10.3, "w_CaF2": 7, "w_MgF2": 0.3, "w_KF": 0.1, "w_LiF": 0,
                               "bath_temp_K": 964 + 273.15}

        self.sliders = {}
        self.labels = {}
        self.result_labels = {}

        for i, attribute in enumerate(self.attributes):
            if attribute == "bath_temp_K":
                min_val, max_val = 1050, 1300
            else:
                min_val, max_val = 0, 10

            self.labels[attribute] = tk.Label(root, text=f"{attribute} : {self.initial_values[attribute]:.2f}")
            self.labels[attribute].grid(row=i + 1, column=0)

            self.sliders[attribute] = ttk.Scale(root, from_=min_val, to=max_val, length=200, orient="horizontal")
            self.sliders[attribute].set(self.initial_values[attribute])
            self.sliders[attribute].grid(row=i + 1, column=1, columnspan=2)

            self.result_labels[attribute] = tk.Label(root, text="")
            self.result_labels[attribute].grid(row=i + 1, column=3)

        self.calculate_button = tk.Button(root, text="Calculate", command=self.update_results)
        self.calculate_button.grid(row=len(self.attributes) + 1, column=0, columnspan=2)

        self.update_results()

    def update_results(self):
        for attribute in self.attributes:
            if attribute == "bath_temp_K":
                self.bath.bath_temp_K = self.sliders[attribute].get() + 273.15
            else:
                setattr(self.bath, attribute, self.sliders[attribute].get())

            self.labels[attribute].config(text=f"{attribute} : {self.sliders[attribute].get():.2f}")

        self.result_labels["bath_conductivity"].config(text=f"bath_conductivity : {self.bath.bath_conductivity():.4f}")
        self.result_labels["bath_resistivity"].config(text=f"bath_resistivity : {self.bath.bath_resistivity():.4f}")
        self.result_labels["Al2O3_solub_A_factor"].config(text=f"Al2O3_solub_A_factor : {self.bath.Al2O3_solub_A_factor():.4f}")
        self.result_labels["Al2O3_solub_B_factor"].config(text=f"Al2O3_solub_B_factor : {self.bath.Al2O3_solub_B_factor():.4f}")
        self.result_labels["Al2O3_sat"].config(text=f"Al2O3_sat : {self.bath.Al2O3_sat():.4f}")
        self.result_labels["Al2O3_rel_sat"].config(text=f"Al2O3_rel_sat : {self.bath.Al2O3_rel_sat():.4f}")
        self.result_labels["Equil_potential"].config(text=f"Equil_potential : {self.bath.Equil_potential():.4f}")

if __name__ == "__main__":
    root = tk.Tk()
    app = BathGUI(root)
    root.mainloop()
