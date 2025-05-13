import customtkinter
import customtkinter as ctk
from PIL import Image, ImageTk
from tkinter import PhotoImage
import tkinter as tk
import csv

class MyRadiobuttonFrame(customtkinter.CTkFrame):
    def __init__(self, master, title, values):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.configure(fg_color="transparent")

        self.title = customtkinter.CTkLabel(self, text=title, fg_color="gray30", corner_radius=6)
        self.title.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.radiobuttons = []  # Liste, um die Radiobuttons zu speichern
        self.variable = customtkinter.StringVar(value=None)  # Verwende customtkinter.StringVar
        self.create_radiobuttons(values)

    def create_radiobuttons(self, values):
        for i, value in enumerate(values):
            radiobutton = customtkinter.CTkRadioButton(self, text=value, variable=self.variable, value=value)
            radiobutton.grid(row=i + 1, column=0, padx=20, pady=(0, 20), sticky="w")
            self.radiobuttons.append(radiobutton)  # Speichere die Radiobuttons

    def get(self):
        return self.variable.get()

    def update_values(self, new_values):
        # Zerstöre alle vorhandenen Radiobuttons
        for button in self.radiobuttons:
            button.destroy()
        self.radiobuttons = []  # Leere die Liste

        # Erstelle neue Radiobuttons mit den neuen Werten
        self.create_radiobuttons(new_values)

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("War Thunder Wiki")
        self.geometry("1200x600")

        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)

        # Bestehende Nationen und Flugzeuge
        values = ["Germany", "USA", "USSR"]
        self.nation_options = {
            "Germany": ["Airplane 1", "Airplane 2", "Airplane 3", "Airplane 4", "Airplane 5"],
            "USA": ["Airplane 1", "Airplane 2", "Airplane 3", "Airplane 4"],
            "USSR": ["Airplane 1", "Airplane 2", "Airplane 3", "Airplane 4"],
        }

        # Radiobutton Frame für Nationen
        self.radiobutton_frame = MyRadiobuttonFrame(self, "Nations", values=values)
        self.radiobutton_frame.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsew")
        self.radiobutton_frame.variable.trace("w", self.on_nation_selected)

        # Radiobutton Frame für Flugzeuge
        self.radiobutton_frame_options = MyRadiobuttonFrame(self, "Airplanes", values=[])
        self.radiobutton_frame_options.grid(row=1, column=0, padx=(0, 10), pady=(10, 0), sticky="nsew")

        # Button zum Bestätigen der Auswahl
        self.confirm_button = customtkinter.CTkButton(self, text="Confirm", command=self.confirm_selection)
        self.confirm_button.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        # Button zum Hinzufügen einer Auswahl
        self.add_button = customtkinter.CTkButton(self, text="Add", command=self.add_selection)
        self.add_button.grid(row=3, column=0, padx=5, pady=5, sticky="ew")

        # Bild- und Informationsfenster
        self.setup_info_and_image_frames()

        # Initialisiere Bilder und Texte
        self.setup_images_and_texts()

    def setup_info_and_image_frames(self):
        # Bildfenster
        self.image_frame = customtkinter.CTkFrame(self)
        self.image_frame.grid(row=0, column=1, padx=10, pady=10)
        self.image_frame.grid_columnconfigure(0, weight=1)
        self.image_frame.grid_rowconfigure(0, weight=1)
        self.image_label = customtkinter.CTkLabel(self.image_frame, text="", image=None)
        self.image_label.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Informationsfenster
        self.info_frame = customtkinter.CTkFrame(self)
        self.info_frame.grid(row=1, column=1, padx=10, pady=10)
        self.info_frame.grid_columnconfigure(0, weight=1)
        self.info_frame.grid_rowconfigure(0, weight=1)
        self.info_label = customtkinter.CTkLabel(self.info_frame, text="")
        self.info_label.grid(row=1, column=1, padx=10, pady=10)

    def setup_images_and_texts(self):
        self.images = {
            "Germany": {
                "Airplane 1": "tornado-und-eurofighter.png",
                "Airplane 2": "image_deutschland_option2.png",
                "Airplane 3": "image_deutschland_option3.png",
                "Airplane 4": "image_deutschland_option4.png",
                "Airplane 5": "image_deutschland_option5.png"
            },
            "USA": {
                "Airplane 1": "image_usa_option1.png",
                "Airplane 2": "image_usa_option2.png",
                "Airplane 3": "image_usa_option3.png",
                "Airplane 4": "image_usa_option4.png",
            },
            "USSR": {
                "Airplane 1": "image_russland_option1.png",
                "Airplane 2": "image_russland_option2.png",
                "Airplane 3": "image_russland_option3.png",
                "Airplane 4": "image_russland_option4.png"
            }
        }
        self.info_texts = {
            "Germany": {
                "Airplane 1": "Informationen zu Deutschland Option 1",
                "Airplane 2": "Informationen zu Deutschland Option 2",
                "Airplane 3": "Informationen zu Deutschland Option 3",
                "Airplane 4": "Informationen zu Deutschland Option 4",
                "Airplane 5": "Informationen zu Deutschland Option 5"
            },
            "USA": {
                "Airplane 1": "Informationen zu USA Option 1",
                "Airplane 2": "Informationen zu USA Option 2",
                "Airplane 3": "Informationen zu USA Option 3",
                "Airplane 4": "Informationen zu USA Option 4"
            },
            "USSR": {
                "Airplane 1": "Informationen zu Russland Option 1",
                "Airplane 2": "Informationen zu Russland Option 2",
                "Airplane 3": "Informationen zu Russland Option 3",
                "Airplane 4": "Informationen zu Russland Option 4"
            }
        }

    def add_selection(self):
        add_dialog = AddSelectionDialog(self)  # Dialog zur Eingabe neuer Nation und Flugzeug
        self.wait_window(add_dialog)  # Warte, bis der Dialog geschlossen ist

        if add_dialog.nation and add_dialog.airplane:
            new_nation = add_dialog.nation
            new_airplane = add_dialog.airplane

            # Füge die neue Nation und das Flugzeug hinzu
            if new_nation not in self.nation_options:
                self.nation_options[new_nation] = []
            if new_airplane not in self.nation_options[new_nation]:
                self.nation_options[new_nation].append(new_airplane)

            # Aktualisiere Radiobutton Optionen
            self.update_nation_options()

            # Bestätigungsnachricht
            self.info_label.configure(text=f"Neue Auswahl hinzugefügt: {new_nation}, {new_airplane}")

    def update_nation_options(self):
        # Aktualisiere die Nationen Radiobuttons
        self.radiobutton_frame.update_values(list(self.nation_options.keys()))
        # Wenn die neu hinzugefügte Nation ausgewählt ist, aktualisiere die Flugzeugoptionen
        selected_nation = self.radiobutton_frame.get()
        self.update_options(selected_nation)

    def update_options(self, selected_nation):
        if selected_nation:
            options = self.nation_options.get(selected_nation, [])
            self.radiobutton_frame_options.destroy()
            self.radiobutton_frame_options = MyRadiobuttonFrame(self, "Airplanes", values=options)
            self.radiobutton_frame_options.grid(row=1, column=0, padx=(0, 10), pady=(10, 0), sticky="nsew")

    def on_nation_selected(self, *args):
        selected_nation = self.radiobutton_frame.get()
        self.update_options(selected_nation)

    def confirm_selection(self):
        nation = self.radiobutton_frame.get()
        option = self.radiobutton_frame_options.get()

        if nation and option:
            self.display_image_and_info(nation, option)
        else:
            self.info_label.configure(text="Please select a Nation and an Airplane.")
            self.image_label.configure(image=None, text="")

    def display_image_and_info(self, nation, option):
        image_path = self.images.get(nation, {}).get(option)
        info_text = self.info_texts.get(nation, {}).get(option)

        if image_path:
            try:
                image = Image.open(image_path)
                photo = ImageTk.PhotoImage(image)
                self.image_label.configure(image=photo, text="")
                self.image_label.image = photo  # Wichtig: Referenz behalten!
            except FileNotFoundError:
                self.image_label.configure(text="Image not found.")
                self.image_label.image = None
        else:
            self.image_label.configure(text="No image available.")
            self.image_label.image = None

        if info_text:
            self.info_label.configure(text=info_text)
        else:
            self.info_label.configure(text="No info available.")
app = App()
app.mainloop()
