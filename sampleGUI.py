import tkinter as tk

class Person:
    def __init__(self, name, age, occupation):
        self.name = name
        self.age = age
        self.occupation = occupation

    def greet(self):
        return f"Hello, my name is {self.name}. I am {self.age} years old, and I work as a {self.occupation}."

class SampleGUI:
    def __init__(self, root, person):
        self.root = root
        self.person = person
        self.create_widgets()

    def create_widgets(self):
        self.name_label = tk.Label(self.root, text="Name:")
        self.name_label.grid(row=0, column=0)
        self.name_entry = tk.Entry(self.root)
        self.name_entry.grid(row=0, column=1)

        self.age_label = tk.Label(self.root, text="Age:")
        self.age_label.grid(row=1, column=0)
        self.age_entry = tk.Entry(self.root)
        self.age_entry.grid(row=1, column=1)

        self.occupation_label = tk.Label(self.root, text="Occupation:")
        self.occupation_label.grid(row=2, column=0)
        self.occupation_entry = tk.Entry(self.root)
        self.occupation_entry.grid(row=2, column=1)

        self.update_button = tk.Button(self.root, text="Update", command=self.update_attributes)
        self.update_button.grid(row=3, column=0, columnspan=2)

        self.output_box = tk.Text(self.root, height=5, width=30)
        self.output_box.grid(row=4, column=0, columnspan=2)

        # Initialize the entry fields with current attribute values
        self.name_entry.insert(0, self.person.name)
        self.age_entry.insert(0, self.person.age)
        self.occupation_entry.insert(0, self.person.occupation)

        # Display the initial greeting in the output box
        self.update_output_box()

    def update_attributes(self):
        # Update the attribute values with the values entered in the entry fields
        self.person.name = self.name_entry.get()
        self.person.age = self.age_entry.get()
        self.person.occupation = self.occupation_entry.get()

        # Display the updated greeting in the output box
        self.update_output_box()

    def update_output_box(self):
        greeting = self.person.greet()
        self.output_box.delete(1.0, tk.END)
        self.output_box.insert(tk.END, greeting)

if __name__ == "__main__":
    # Sample Person object
    person = Person(name="John Doe", age=30, occupation="Software Engineer")

    # Create the main window
    root = tk.Tk()
    root.title("Sample GUI")

    # Create the SampleGUI instance
    sample_gui = SampleGUI(root, person)

    # Start the GUI main loop
    root.mainloop()
