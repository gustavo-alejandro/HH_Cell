import tkinter as tk
from tkinter import ttk
import math
from PIL import Image, ImageTk

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
        attributes_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="w")

        attributes_labels = ['w_Al2O3', 'w_AlF3', 'w_CaF2', 'w_MgF2', 'w_KF', 'w_LiF', 'Temperature (K)']
        attributes_vars = [self.w_Al2O3, self.w_AlF3, self.w_CaF2, self.w_MgF2, self.w_KF, self.w_LiF, self.temperature_K]

        for idx, label in enumerate(attributes_labels):
            ttk.Label(attributes_frame, text=label).grid(row=idx, column=0, padx=5, pady=5)
            ttk.Scale(attributes_frame, variable=attributes_vars[idx], from_=0, to=10, length=200, orient="horizontal").grid(row=idx, column=1, padx=5, pady=5)
            ttk.Label(attributes_frame, textvariable=attributes_vars[idx]).grid(row=idx, column=2, padx=5, pady=5)

        # Display boxes for bath conductivity and bath resistivity
        conductivity_frame = ttk.LabelFrame(self.root, text="Bath Conductivity")
        conductivity_frame.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        self.conductivity_label = ttk.Label(conductivity_frame, text="Bath Conductivity: ")
        self.conductivity_label.grid(row=0, column=0, padx=5, pady=5)

        resistivity_frame = ttk.LabelFrame(self.root, text="Bath Resistivity")
        resistivity_frame.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        self.resistivity_label = ttk.Label(resistivity_frame, text="Bath Resistivity: ")
        self.resistivity_label.grid(row=0, column=0, padx=5, pady=5)

        ttk.Button(self.root, text="Calculate", command=self.update_results).grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def update_results(self):
        conductivity = self.bath_conductivity()
        resistivity = self.bath_resistivity()

        self.conductivity_label.config(text=f"Bath Conductivity: {conductivity:.4f}")
        self.resistivity_label.config(text=f"Bath Resistivity: {resistivity:.4f}")

if __name__ == "__main__":
    root = tk.Tk()
    bath_gui = BathGUI(root)
    root.mainloop()
