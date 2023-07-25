import tkinter as tk
from tkinter import ttk
import math

class BathGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Bath Attributes GUI")

        # Initialize attribute values
        self.w_Al2O3 = tk.DoubleVar(value=4.2)
        self.w_AlF3 = tk.DoubleVar(value=10.3)
        self.w_CaF2 = tk.DoubleVar(value=7)
        self.w_MgF2 = tk.DoubleVar(value=0.3)
        self.w_KF = tk.DoubleVar(value=0.1)
        self.w_LiF = tk.DoubleVar(value=0)
        self.temperature_K = tk.DoubleVar(value=964+273.15)

        self.create_widgets()

    def bath_conductivity(self):
        w_Al2O3 = self.w_Al2O3.get()
        w_AlF3 = self.w_AlF3.get()
        w_CaF2 = self.w_CaF2.get()
        w_MgF2 = self.w_MgF2.get()
        w_KF = self.w_KF.get()
        w_LiF = self.w_LiF.get()
        temperature = self.temperature_K.get()

        # Calculate the bath conductivity using the provided equation
        bath_conductivity = math.exp(1.977 - 0.02 * w_Al2O3 - 0.0131 * w_AlF3 - 0.006 * w_CaF2 - 0.0106 * w_MgF2 - 0.0019 * w_KF + 0.0121 * w_LiF - 1204.3 / temperature)
        return bath_conductivity

    def bath_resistivity(self):
        bath_conductivity = self.bath_conductivity()

        # Calculate the bath resistivity
        bath_resistivity = 1 / bath_conductivity
        return bath_resistivity

    def create_widgets(self):
        attributes_frame = ttk.LabelFrame(self.root, text="Attributes")
        attributes_frame.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        ttk.Label(attributes_frame, text="w_Al2O3").grid(row=0, column=0, padx=5, pady=5)
        ttk.Scale(attributes_frame, variable=self.w_Al2O3, from_=0, to=10, length=200, orient="horizontal").grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(attributes_frame, textvariable=self.w_Al2O3).grid(row=0, column=2, padx=5, pady=5)

        ttk.Label(attributes_frame, text="w_AlF3").grid(row=1, column=0, padx=5, pady=5)
        ttk.Scale(attributes_frame, variable=self.w_AlF3, from_=0, to=10, length=200, orient="horizontal").grid(row=1, column=1, padx=5, pady=5)
        ttk.Label(attributes_frame, textvariable=self.w_AlF3).grid(row=1, column=2, padx=5, pady=5)

        ttk.Label(attributes_frame, text="w_CaF2").grid(row=2, column=0, padx=5, pady=5)
        ttk.Scale(attributes_frame, variable=self.w_CaF2, from_=0, to=10, length=200, orient="horizontal").grid(row=2, column=1, padx=5, pady=5)
        ttk.Label(attributes_frame, textvariable=self.w_CaF2).grid(row=2, column=2, padx=5, pady=5)

        ttk.Label(attributes_frame, text="w_MgF2").grid(row=3, column=0, padx=5, pady=5)
        ttk.Scale(attributes_frame, variable=self.w_MgF2, from_=0, to=10, length=200, orient="horizontal").grid(row=3, column=1, padx=5, pady=5)
        ttk.Label(attributes_frame, textvariable=self.w_MgF2).grid(row=3, column=2, padx=5, pady=5)

        ttk.Label(attributes_frame, text="w_KF").grid(row=4, column=0, padx=5, pady=5)
        ttk.Scale(attributes_frame, variable=self.w_KF, from_=0, to=10, length=200, orient="horizontal").grid(row=4, column=1, padx=5, pady=5)
        ttk.Label(attributes_frame, textvariable=self.w_KF).grid(row=4, column=2, padx=5, pady=5)

        ttk.Label(attributes_frame, text="w_LiF").grid(row=5, column=0, padx=5, pady=5)
        ttk.Scale(attributes_frame, variable=self.w_LiF, from_=0, to=10, length=200, orient="horizontal").grid(row=5, column=1, padx=5, pady=5)
        ttk.Label(attributes_frame, textvariable=self.w_LiF).grid(row=5, column=2, padx=5, pady=5)

        ttk.Label(attributes_frame, text="Temperature (K)").grid(row=6, column=0, padx=5, pady=5)
        ttk.Scale(attributes_frame, variable=self.temperature_K, from_=800+273.15, to=1000+273.15, length=200, orient="horizontal").grid(row=6, column=1, padx=5, pady=5)
        ttk.Label(attributes_frame, textvariable=self.temperature_K).grid(row=6, column=2, padx=5, pady=5)

        # Display boxes for bath conductivity and bath resistivity
        conductivity_frame = ttk.LabelFrame(self.root, text="Bath Conductivity")
        conductivity_frame.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.conductivity_label = ttk.Label(conductivity_frame, text="Bath Conductivity: ")
        self.conductivity_label.grid(row=0, column=0, padx=5, pady=5)

        resistivity_frame = ttk.LabelFrame(self.root, text="Bath Resistivity")
        resistivity_frame.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        self.resistivity_label = ttk.Label(resistivity_frame, text="Bath Resistivity: ")
        self.resistivity_label.grid(row=0, column=0, padx=5, pady=5)

        ttk.Button(self.root, text="Calculate", command=self.update_results).grid(row=3, column=0, padx=10, pady=10)

    def update_results(self):
        conductivity = self.bath_conductivity()
        resistivity = self.bath_resistivity()

        self.conductivity_label.config(text=f"Bath Conductivity: {conductivity:.4f}")
        self.resistivity_label.config(text=f"Bath Resistivity: {resistivity:.4f}")

if __name__ == "__main__":
    root = tk.Tk()
    bath_gui = BathGUI(root)
    root.mainloop()
