import tkinter as tk
from tkinter import ttk
import math


class BathGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Bath Attributes GUI")

        # Initial values for attributes
        self.w_Al2O3 = tk.DoubleVar(value=5.0)
        self.w_AlF3 = tk.DoubleVar(value=5.0)
        self.w_CaF2 = tk.DoubleVar(value=5.0)
        self.w_MgF2 = tk.DoubleVar(value=5.0)
        self.w_KF = tk.DoubleVar(value=5.0)
        self.w_LiF = tk.DoubleVar(value=5.0)
        self.temperature = tk.DoubleVar(value=300.0)

        self.create_widgets()

    def bath_resistance(self):
        w_Al2O3 = self.w_Al2O3.get()
        w_AlF3 = self.w_AlF3.get()
        w_CaF2 = self.w_CaF2.get()
        w_MgF2 = self.w_MgF2.get()
        w_KF = self.w_KF.get()
        w_LiF = self.w_LiF.get()
        temperature = self.temperature.get()

        # Calculate the bath resistance using the provided equation
        bath_resistance = math.exp(
            1.977 - 0.02 * w_Al2O3 - 0.0131 * w_AlF3 - 0.006 * w_CaF2 - 0.0106 * w_MgF2 - 0.0019 * w_KF + 0.0121 * w_LiF - 1204.3 / temperature)
        return bath_resistance

    def create_widgets(self):
        # Slider widgets for each attribute
        attributes_frame = ttk.LabelFrame(self.root, text="Attributes")
        attributes_frame.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        ttk.Label(attributes_frame, text="w_Al2O3").grid(row=0, column=0, padx=5, pady=5)
        ttk.Scale(attributes_frame, variable=self.w_Al2O3, from_=0, to=10, length=200, orient="horizontal").grid(row=0,
                                                                                                                 column=1,
                                                                                                                 padx=5,
                                                                                                                 pady=5)

        ttk.Label(attributes_frame, text="w_AlF3").grid(row=1, column=0, padx=5, pady=5)
        ttk.Scale(attributes_frame, variable=self.w_AlF3, from_=0, to=10, length=200, orient="horizontal").grid(row=1,
                                                                                                                column=1,
                                                                                                                padx=5,
                                                                                                                pady=5)

        ttk.Label(attributes_frame, text="w_CaF2").grid(row=2, column=0, padx=5, pady=5)
        ttk.Scale(attributes_frame, variable=self.w_CaF2, from_=0, to=10, length=200, orient="horizontal").grid(row=2,
                                                                                                                column=1,
                                                                                                                padx=5,
                                                                                                                pady=5)

        ttk.Label(attributes_frame, text="w_MgF2").grid(row=3, column=0, padx=5, pady=5)
        ttk.Scale(attributes_frame, variable=self.w_MgF2, from_=0, to=10, length=200, orient="horizontal").grid(row=3,
                                                                                                                column=1,
                                                                                                                padx=5,
                                                                                                                pady=5)

        ttk.Label(attributes_frame, text="w_KF").grid(row=4, column=0, padx=5, pady=5)
        ttk.Scale(attributes_frame, variable=self.w_KF, from_=0, to=10, length=200, orient="horizontal").grid(row=4,
                                                                                                              column=1,
                                                                                                              padx=5,
                                                                                                              pady=5)

        ttk.Label(attributes_frame, text="w_LiF").grid(row=5, column=0, padx=5, pady=5)
        ttk.Scale(attributes_frame, variable=self.w_LiF, from_=0, to=10, length=200, orient="horizontal").grid(row=5,
                                                                                                               column=1,
                                                                                                               padx=5,
                                                                                                               pady=5)

        ttk.Label(attributes_frame, text="Temperature").grid(row=6, column=0, padx=5, pady=5)
        ttk.Scale(attributes_frame, variable=self.temperature, from_=0, to=1000, length=200, orient="horizontal").grid(
            row=6, column=1, padx=5, pady=5)

        # Display box for the bath resistance
        resistance_frame = ttk.LabelFrame(self.root, text="Bath Resistance")
        resistance_frame.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        self.resistance_label = ttk.Label(resistance_frame, text="Bath Resistance: ")
        self.resistance_label.grid(row=0, column=0, padx=5, pady=5)

        ttk.Button(self.root, text="Calculate Resistance", command=self.update_resistance).grid(row=2, column=0,
                                                                                                padx=10, pady=10)

    def update_resistance(self):
        resistance = self.bath_resistance()
        self.resistance_label.config(text=f"Bath Resistance: {resistance:.4f}")


if __name__ == "__main__":
    root = tk.Tk()
    bath_gui = BathGUI(root)
    root.mainloop()
