import customtkinter as ctk
#import tkintertable as tkt #Weiss noch nicht ob das mit ctk läuft
import CSVWorker as cw
import Class_Structure

# Flugzeugdaten laden
filename_aircraft = 'Aircraft.csv'  #  Dateipfad
filename_armament = 'Armament.csv'
filename_hardpoint_selected = '' #ändert sich im Laufe des Programms
filename_hardpoint = f'{filename_hardpoint_selected}_Hardpoints.csv' #damit es flexibel ist
aircraft_data = cw.import_aircraft(filename_aircraft)
armament_data = cw.import_armaments(filename_armament)

if aircraft_data is None:
    print("Fehler: Konnte die Flugzeugdaten nicht laden.")
    exit()  # Beende das Programm, wenn die Daten nicht geladen werden konnten

class FlugzeugDatenApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.delete_window = None
        self.title("Wiki")
        self.geometry("800x600")  # Fenster größe
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)  # Für das Textfeld

        self.grid_rowconfigure(0, weight=1)  # Für das Hauptfenster
        self.grid_rowconfigure(1, weight=1)  # Für das Hauptfenster

        self.selected_nation = None
        self.selected_flugzeug = None
        self.selected_waffe = None

        self.update_parameters()
        self.create_widgets()

    def update_filename_hardpoint(self, flugzeug):
        filename_hardpoint_selected = flugzeug
        filename_hardpoint = f'{filename_hardpoint_selected}_Hardpoints.csv'

        try:
            hardpoint_data = cw.import_hardpoints(filename_hardpoint)
            hardpoint_data_string = ""
            for i in hardpoint_data:
                hardpoint_data_string += (f'{i.amount}, {i.name}, {i.pylon_ges_anz}, {i.pylon_bool}, \n')
            return hardpoint_data_string
        except:
            return None

    def update_parameters(self):
        print("update_parameters")
        self.nationen = None
        self.nationen = sorted({flugzeug.nation for flugzeug in aircraft_data})
        self.flugzeuge_pro_nation = {
            nation: sorted({flugzeug.name for flugzeug in aircraft_data if flugzeug.nation == nation})
            for nation in self.nationen
        }
        self.aircraft = sorted({flugzeug.name for flugzeug in aircraft_data})

        self.weapon_types = sorted({weapon.armament_type for weapon in armament_data})
        self.waffen_pro_type = {
            type: sorted({weapon.name for weapon in armament_data if weapon.armament_type == type})
            for type in self.weapon_types
        }

    def create_widgets(self):
        # Linke Seite: Auswahlbereiche
        self.frame_links = ctk.CTkFrame(master=self, width=200)
        #Reihe 0 (ganz links), Spalte 0 (ganz oben), Soll über beide Reihen gehen
        self.frame_links.grid(row=0, column=0, rowspan=2, padx=20, pady=20, sticky="nsew")

        self.nationen_label = ctk.CTkLabel(master=self.frame_links, text="Wiki auswählen:")
        self.nationen_label.pack(pady=10)

        self.wiki_checker = ctk.CTkOptionMenu(master=self.frame_links, values=['Flugzeuge', 'Waffen'], state='normal',
                                              command=self.choose_wiki)  # state = normal
        self.wiki_checker.pack(pady=10)
        self.wiki_checker.set('')

    def choose_wiki(self, auswahl):
        #if hasattr(self, 'nationen_entry'):
        for widget in self.frame_links.winfo_children():
            widget.destroy()
        try:
            self.text_area.destroy()                            #Löscht das Textfeld (Falls vorhanden)
        except:
            pass

        try:
            self.text_area_pylon.destroy()                      #Loscht das zweite Textfeld (falls vorhanden)
        except:
            pass

        self.nationen_label = ctk.CTkLabel(master=self.frame_links, text="Wiki auswählen:")
        self.nationen_label.pack(pady=10)

        self.wiki_checker = ctk.CTkOptionMenu(master=self.frame_links, values=['Flugzeuge', 'Waffen'], state='normal',
                                              command=self.choose_wiki)  # state = normal
        self.wiki_checker.pack(pady=10)
        self.wiki_checker.set('')

        if auswahl == "Flugzeuge":
            self.create_widgets_flugzeuge()

        elif auswahl == "Waffen":
            self.create_widgets_waffen()

    def create_widgets_flugzeuge(self):

        self.nationen_label = ctk.CTkLabel(master=self.frame_links, text="Nation auswählen:")
        self.nationen_label.pack(pady=10)

        self.nationen_combobox = ctk.CTkOptionMenu(master=self.frame_links, values=self.nationen,command=self.nation_ausgewaehlt)
        self.nationen_combobox.pack(pady=10)
        self.nationen_combobox.set('')

        self.flugzeuge_label = ctk.CTkLabel(master=self.frame_links, text="Flugzeug auswählen:")
        self.flugzeuge_label.pack(pady=10)

        self.flugzeuge_combobox = ctk.CTkOptionMenu(master=self.frame_links, values=[], state='normal',command=self.flugzeug_ausgewaehlt)  # state = normal
        self.flugzeuge_combobox.pack(pady=10)
        self.flugzeuge_combobox.set('')

        self.confirm_button = ctk.CTkButton(master=self.frame_links, text="Bestätigen", command=self.zeige_flugzeug_daten)
        self.confirm_button.pack(pady=20)

        self.add_button_flieger = ctk.CTkButton(master=self.frame_links, text="Add Nation/Flugzeug",
                                        command=self.open_add_aircraft)
        self.add_button_flieger.pack(pady=10)

        self.edit_button =ctk.CTkButton(master=self.frame_links,text="Edit Nation/Flugzeug",command = self.open_edit_aircraft)
        self.edit_button.pack(pady=10)

        self.delete_button = ctk.CTkButton(master=self.frame_links, text="Löschen", command=self.open_delete_aircraft)
        self.delete_button.pack(pady=10)

#Oben: Daten Flugzeug______________________________________________________________________________________________________________________________
        self.text_area = ctk.CTkTextbox(master=self, width=400, wrap="word")
        self.text_area.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.text_area.configure(state="disabled")  # Damit das Textfeld von anfang an nicht bearbeitet werden kann
# Unten: Daten Pylon________________________________________________________________________________________________________________________________
        self.text_area_pylon = ctk.CTkTextbox(master=self, width=400, wrap="word")
        self.text_area_pylon.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")
        self.text_area_pylon.configure(state="disabled")  #Damit das Textfeld von anfang an nicht bearbeitet werden kann
    #___________________________________________________________________________________________________________________________________________________
    def create_widgets_waffen(self):
        self.waffen_label = ctk.CTkLabel(master=self.frame_links, text="Waffentyp auswählen:")
        self.waffen_label.pack(pady=10)

        self.weapon_type_option = ctk.CTkOptionMenu(master=self.frame_links, values=self.weapon_types, state='normal',command=self.armament_type_ausgewaehlt)  # state = normal
        self.weapon_type_option.pack(pady=10)
        self.weapon_type_option.set('')

        self.flugzeuge_label = ctk.CTkLabel(master=self.frame_links, text="Waffe auswählen:")
        self.flugzeuge_label.pack(pady=10)

        self.waffen_option = ctk.CTkOptionMenu(master=self.frame_links, values=[], state='normal',command=self.waffe_ausgewählt)  # state = normal
        self.waffen_option.pack(pady=10)
        self.waffen_option.set('')

        self.confirm_button = ctk.CTkButton(master=self.frame_links, text="Bestätigen", command=self.zeige_waffen_daten)
        self.confirm_button.pack(pady=20)

        self.add_button_waffen = ctk.CTkButton(master=self.frame_links, text="Add Armament",command=self.open_edit_aircraft)
        self.add_button_waffen.pack(pady=10)
        self.add_button_waffen.configure(state="disabled")

        self.edit_armament_button = ctk.CTkButton(master=self.frame_links, text="Edit Armament",command=self.open_edit_aircraft)
        self.edit_armament_button.pack(pady=10)
        self.edit_armament_button.configure(state="disabled")

        self.delete_button = ctk.CTkButton(master=self.frame_links, text="Löschen", command=self.open_delete_aircraft)
        self.delete_button.pack(pady=10)
        self.delete_button.configure(state="disabled")
        # Oben: Daten Flugzeug______________________________________________________________________________________________________________________________
        self.text_area = ctk.CTkTextbox(master=self, width=400, wrap="word")
        self.text_area.grid(row=0, column=1, rowspan =2,  padx=20, pady=20, sticky="nsew")
        self.text_area.configure(state="disabled")  # Damit das Textfeld von anfang an nicht bearbeitet werden kann
    #___________________________________________________________________________________________________________________________________________________
    def nation_ausgewaehlt(self, nation):
        self.selected_nation = nation
        self.flugzeuge_combobox.configure(values=self.flugzeuge_pro_nation.get(nation, [])) #(Output)Flugzeuge der ausgewählten nation                             #Dropdown menü (Nation)     # Setze die Auswahl zurück
        self.selected_flugzeug = None
        self.text_area.delete("1.0", "end")      # Lösche den Text
    #____________________________________________________________________________________________________________________________________________________
    def armament_type_ausgewaehlt(self, type):
        self.selected_weapon_type = type
        self.waffen_option.configure(values=self.waffen_pro_type.get(type, []))  # Dropdown menü (Nation)     # Setze die Auswahl zurück
        self.text_area.delete("1.0", "end")  # Lösche den Text
# ____________________________________________________________________________________________________________________________________________________
    def flugzeug_ausgewaehlt(self, flugzeug):
        self.selected_flugzeug = flugzeug

    def flugzeug_ausgewaehlt_loeschen(self, flugzeug):
        self.flugzeug_zu_loeschen = flugzeug

    def waffe_ausgewählt(self, waffe):
        self.selected_waffe = waffe

    def waffe_ausgewaehlt_loeschen(self, waffe): #Vorbereitung
        pass

    def zeige_flugzeug_daten(self):
        self.text_area.configure(state="normal") # Normal: Textfeld kann bearbeitet/aktualisiert werden
        self.text_area.delete("1.0", "end")  # Lösche den alten Text

        if self.selected_nation and self.selected_flugzeug:
            #Hardpoint Anzeige
            self.text_area_pylon.configure(state="normal")
            self.text_area_pylon.delete("1.0", "end")
            hardpoint_data = self.update_filename_hardpoint(self.selected_flugzeug)
            if hardpoint_data:
                self.text_area_pylon.insert("1.0", hardpoint_data)
            self.text_area_pylon.configure(state="disabled")


            #Flugzeugdaten
            for zeile in aircraft_data:
                if zeile.nation == self.selected_nation and zeile.name == self.selected_flugzeug:
                    daten_text = "Daten des Flugzeugs:\n"
                    for key, value in vars(zeile).items():
                        daten_text += f"- {key}: {value}\n"
                    self.text_area.insert("1.0", daten_text)
                    self.text_area.configure(state="disabled") # disable : read only
                    return  # Beende die Suche, sobald das Flugzeug gefunden wurde

            self.text_area.insert("1.0", "Flugzeugdaten nicht gefunden.")
        else:
            self.text_area.insert("1.0", "Bitte wähle eine Nation und ein Flugzeug aus.")


    def zeige_waffen_daten(self):
        self.text_area.configure(state="normal") # Normal: Textfeld kann bearbeitet/aktualisiert werden
        self.text_area.delete("1.0", "end")  # Lösche den alten Text
        if self.selected_weapon_type and self.selected_waffe:
            for zeile in armament_data:
                if zeile.armament_type == self.selected_weapon_type and zeile.name == self.selected_waffe:
                    daten_text = "Daten der Waffe:\n"
                    for key, value in vars(zeile).items():
                        daten_text += f"- {key}: {value}\n"
                    self.text_area.insert("1.0", daten_text)
                    self.text_area.configure(state="disabled") # disable : read only
                    return  # Beende die Suche, sobald das Flugzeug gefunden wurde

            self.text_area.insert("1.0", "Waffendaten nicht gefunden.")
        else:
            self.text_area.insert("1.0", "Bitte wähle einen Waffentyp und eine Waffe aus.")
#______________________________________________________________________________________________________________________________________________________
    def open_add_aircraft(self):
        self.add_window = ctk.CTkToplevel(self)
        self.add_window.title("Add Nation/Flugzeug")
        self.add_window.geometry("400x650")

        self.nationen_checklabel = ctk.CTkLabel(master=self.add_window, text="Ist es eine neue Nation?:")
        self.nationen_checklabel.pack(pady=10)

        self.neue_nation_checker = ctk.CTkOptionMenu(master=self.add_window,values=("ja", "nein"),command=self.neue_nation_checktask)
        self.neue_nation_checker.pack(pady=10)
        self.neue_nation_checker.set('Bitte auswählen')

    def open_edit_aircraft(self):
        self.add_window = ctk.CTkToplevel(self)
        self.add_window.title("Edit Nation/Flugzeug")
        self.add_window.geometry("400x600")

        self.edit_label = ctk.CTkLabel(master=self.add_window, text="Bitte wähle das Flugzeug aus.")
        self.edit_label.pack(pady=10)

        self.edit_checker = ctk.CTkOptionMenu(master=self.add_window,values=self.aircraft,command=self.edit_aircraft)
        self.edit_checker.pack(pady=10)
        self.edit_checker.set('Bitte auswählen')

        self.open_aircraft_structure()


    def open_aircraft_structure(self):

        self.flugzeug_entry = ctk.CTkEntry(master=self.add_window, placeholder_text="Neues Flugzeug")
        self.flugzeug_entry.pack(pady=10)

        # Eingabefelder für die Flugzeugdaten
        self.battle_rating_entry = ctk.CTkEntry(master=self.add_window, placeholder_text="Battle Rating")
        self.battle_rating_entry.pack(pady=5)

        self.klasse_entry = ctk.CTkEntry(master=self.add_window, placeholder_text="Klasse")
        self.klasse_entry.pack(pady=5)

        self.turnrate_entry = ctk.CTkEntry(master=self.add_window, placeholder_text="Turnrate")
        self.turnrate_entry.pack(pady=5)

        self.steigrate_entry = ctk.CTkEntry(master=self.add_window, placeholder_text="Steigrate")
        self.steigrate_entry.pack(pady=5)

        self.geschwindigkeit_entry = ctk.CTkEntry(master=self.add_window, placeholder_text="Geschwindigkeit")
        self.geschwindigkeit_entry.pack(pady=5)

        self.bei_hoehe_entry = ctk.CTkEntry(master=self.add_window, placeholder_text="bei Höhe")
        self.bei_hoehe_entry.pack(pady=5)

        self.max_hoehe_entry = ctk.CTkEntry(master=self.add_window, placeholder_text="max Höhe")
        self.max_hoehe_entry.pack(pady=5)

        self.anfrage_armament_text = ctk.CTkLabel(master=self.add_window, text="Hat das neue Flugzeug Hardpoints?")
        self.anfrage_armament_text.pack(pady=5)

        self.confirm_add_hardpoints = "Error" #Falls anfrage_armament nicht angefasst wird.

        self.anfrage_armament = ctk.CTkOptionMenu(master=self.add_window,values=("ja", "nein"), command = self.change_confirm_button)
        self.anfrage_armament.pack(pady=10)
        self.anfrage_armament.set('Bitte auswählen')

        self.confirm_add_button = ctk.CTkButton(master=self.add_window, text="Confirm", command=self.bestaetigen)
        self.confirm_add_button.pack(pady=20)

    def change_confirm_button(self, auswahl):
        if auswahl == "ja":
            self.confirm_add_hardpoints = True
        elif auswahl == "nein":
            self.confirm_add_hardpoints = False
        else:
            self.confirm_add_hardpoints = "Error"

    def open_add_hardpoints(self):

        self.add_hardpoint_window = ctk.CTkToplevel(self)
        self.add_hardpoint_window.title(f"Edit Hardpoints - {self.selected_flugzeug}")
        self.add_hardpoint_window.geometry("600x600")

        self.num_hardpoints_label = ctk.CTkLabel(self.add_hardpoint_window, text="Anzahl Hardpoints?")
        self.num_hardpoints_label.pack(pady=5)

        self.num_hardpoints_entry = ctk.CTkEntry(master=self.add_hardpoint_window, placeholder_text="Anzahl")
        self.num_hardpoints_entry.pack(pady=5)

        self.num_hardpoints_confirm_button = ctk.CTkButton(master=self.add_hardpoint_window, text="Confirm", command=self.confirm_hardpoint_count)
        self.num_hardpoints_confirm_button.pack(pady=20)


    def confirm_hardpoint_count(self):
        try:
            anzahl = int(self.num_hardpoints_entry.get())
            # Optional: Speichern oder Weiterverarbeitung
            self.hardpoint_count = anzahl
            print(f"{anzahl} Hardpoints bestätigt.")
            self.create_hardpoint_grid(self.hardpoint_count)

        except ValueError:
            # Bei ungültiger Eingabe
            print("Value Error: integer erwartet")
            self.num_hardpoints_label.configure(text="Bitte eine gültige Zahl eingeben.")

    def create_hardpoint_grid(self, anzahl):
        try:
            pass #erst die grids löschen
        except:
            pass

        self.checkbox_frame = ctk.CTkFrame(master=self.add_hardpoint_window)
        self.checkbox_frame.pack(pady=10)

        for i in range(anzahl):
            row = i // 5
            col = i % 5
            checkbox = ctk.CTkCheckBox(master=self.checkbox_frame, text=f"Pylon {i + 1}")
            checkbox.grid(row=row, column=col, padx=5, pady=5)


    def open_weapon_structure(self):
        pass

    '''
    def open_edit_aircraft(self):
        pass
    '''
    def open_edit_weapon(self):
        pass

    def delete_weapon_window(self):
        pass
#________________________________________________________________________________________________________________________________________________________

    def neues_flugzeug_checktask(self, auswahl):

        if auswahl == "ja":
            self.add_armament = ctk.CTkToplevel(self)
            self.add_armament.title("Add Armament")
            self.add_armament.geometry("400x600")

            self.amrament_entry = ctk.CTkOptionMenu(master=self.add_window, placeholder_text="Anzahl Armaments")
            self.nationen_entry.pack(pady=10)

        elif auswahl == "nein":
            self.nationen_entry = ctk.CTkOptionMenu(master=self.add_window, values=self.nationen)
            self.nationen_entry.pack(pady=10)
            self.nationen_entry.set('Nation auswählen')
            self.add_aircraft()

    def open_delete_aircraft(self):

        self.delete_window = ctk.CTkToplevel(self)
        self.delete_window.title("Löschfenster")
        self.delete_window.geometry("360x400")

        self.delete_abfrage = ctk.CTkLabel(master=self.delete_window,text = ("Bitte wählen sie einen Flugzeug aus: "))
        self.delete_abfrage.pack(pady=10)

        self.delete_flugzeug = ctk.CTkOptionMenu(master=self.delete_window, values=self.aircraft, state='normal',command=self.flugzeug_ausgewaehlt_loeschen)  # state = normal
        self.delete_flugzeug.pack(pady=10)
        self.delete_flugzeug.set('')

        self.loeschen = ctk.CTkButton(master=self.delete_window, text="Löschen", command=self.delete_aircraft)
        self.loeschen.pack(pady=10)
#_________________________________________________________________________________________________________________________________________________________


    def add_aircraft(self):
        self.open_aircraft_structure()
        self.confirm_add_button.configure(command=self.bestaetigen)
        self.confirm_add_button.pack(pady=20)

    def edit_aircraft(self, auswahl):
        self.flugzeug_ausgewaehlt(auswahl)
        for entry in armament_data:
            if self.selected_flugzeug == entry.name:
                self.nationen_entry.configure(text=entry.nationen)
                self.flugzeug_entry.configure(text=entry.flugzeug)
                self.battle_rating_entry.configure(text=entry.battle_rating)
                self.klasse_entry.configure(text=entry.klasse)
                self.turnrate_entry.configure(text=entry.turnrate)
                self.steigrate_entry.configure(text=entry.steig)
                self.geschwindigkeit_entry.configure(text=entry.geschwindigkeit)
                self.bei_hoehe_entry.configure(text=entry.bei_hoehe)
                self.max_hoehe_entry.configure(text=entry.max_hoehe)

        self.confirm_add_button.configure(command=self.edit_bestaetigen)
        self.confirm_add_button.pack(pady=20)

    def edit_bestaetigen(self):
        info_flieger = [
            #self.nationen_entry.get(),
            self.flugzeug_entry.get(),
            self.battle_rating_entry.get(),
            self.klasse_entry.get(),
            self.turnrate_entry.get(),
            self.steigrate_entry.get(),
            self.geschwindigkeit_entry.get(),
            self.bei_hoehe_entry.get(),
            self.max_hoehe_entry.get()
        ]
        if not info_flieger[0]: #Eintrag Nation ist leer
            self.text_area.configure(state="normal")
            self.text_area.delete("1.0", "end")
            self.text_area.insert("1.0", "Bitte gib den Namen der Nation ein.")
            self.text_area.configure(state="disabled")
            #self.open_aircraft_structure.destroy()

        elif info_flieger[0] == "Nation auswählen": #Eintrag Nation ist leer
            self.text_area.configure(state="normal")
            self.text_area.delete("1.0", "end")
            self.text_area.insert("1.0", "Bitte gib den Namen der Nation ein.")
            self.text_area.configure(state="disabled")
            #self.open_aircraft_structure.destroy()

        elif any(eintrag == '' for eintrag in info_flieger[1:]):
            self.text_area.configure(state="normal")
            self.text_area.delete("1.0", "end")
            self.text_area.insert("1.0","Bitte gib zusätzliche Informationen ein.")
            self.text_area.configure(state="disabled")
            #self.open_aircraft_structure.destroy()
        else:
            for entry in aircraft_data:
                if (entry.name == self.selected_flugzeug):
                    entry.nation = entry.nation
                    entry.name = self.flugzeug_entry.get()
                    entry.battlerating = self.battle_rating_entry.get()
                    entry.plane_type = self.klasse_entry.get()
                    entry.turnrate = self.turnrate_entry.get()
                    entry.climbrate = self.steigrate_entry.get()
                    entry.speed = self.geschwindigkeit_entry.get()
                    entry.speedheight = self.bei_hoehe_entry.get()
                    entry.maxheight = self.max_hoehe_entry.get()
            cw.export_aircraft(filename_aircraft, aircraft_data)
            self.update_parameters()
            self.add_window.destroy()

    def delete_aircraft(self):
        for entry in aircraft_data:
            if (entry.name == self.flugzeug_zu_loeschen):
                aircraft_data.remove(entry)
                self.text_area.configure(state="normal")
                self.text_area.delete("1.0", "end")
                self.text_area.insert("1.0", "Flugzeug gelöscht!.")
                self.text_area.configure(state="disabled")
                self.delete_window.destroy()
        cw.export_aircraft(filename_aircraft,aircraft_data)
        self.update_parameters()

    def neue_nation_checktask(self, auswahl): #Damit der Button live gecheckt wird
        if hasattr(self, 'nationen_entry'):
            self.nationen_entry.destroy()
            self.flugzeug_entry.destroy()
            self.battle_rating_entry.destroy()
            self.klasse_entry.destroy()
            self.turnrate_entry.destroy()
            self.steigrate_entry.destroy()
            self.geschwindigkeit_entry.destroy()
            self.bei_hoehe_entry.destroy()
            self.max_hoehe_entry.destroy()
            self.confirm_add_button.destroy()
            self.anfrage_armament_text.destroy()
            self.anfrage_armament.destroy()

        if auswahl == "ja":
            self.nationen_entry = ctk.CTkEntry(master=self.add_window, placeholder_text="Nation")
            self.nationen_entry.pack(pady=10)
            self.add_aircraft()
        elif auswahl == "nein":
            self.nationen_entry = ctk.CTkOptionMenu(master=self.add_window, values=self.nationen)
            self.nationen_entry.pack(pady=10)
            self.nationen_entry.set('Nation auswählen')
            self.add_aircraft()
#___________________________________________________________________________________________________________________________________________________
    def bestaetigen(self):
        """Verarbeitet die Eingabe und fügt die Nation hinzu oder zeigt einen Fehler an."""
        info_flieger = [
            self.nationen_entry.get(),
            self.flugzeug_entry.get(),
            self.battle_rating_entry.get(),
            self.klasse_entry.get(),
            self.turnrate_entry.get(),
            self.steigrate_entry.get(),
            self.geschwindigkeit_entry.get(),
            self.bei_hoehe_entry.get(),
            self.max_hoehe_entry.get()
            ]
        print(info_flieger)
        if not info_flieger[0]: #Eintrag Nation ist leer
            self.text_area.configure(state="normal")
            self.text_area.delete("1.0", "end")
            self.text_area.insert("1.0", "Bitte gib den Namen der Nation ein.")
            self.text_area.configure(state="disabled")
            self.add_window.destroy()
            self.open_add_aircraft()

        elif info_flieger[0] == "Nation auswählen": #Eintrag Nation ist leer
            self.text_area.configure(state="normal")
            self.text_area.delete("1.0", "end")
            self.text_area.insert("1.0", "Bitte gib den Namen der Nation ein.")
            self.text_area.configure(state="disabled")
            self.add_window.destroy()
            self.open_add_aircraft()

        elif any(eintrag == '' for eintrag in info_flieger[1:]):
            self.text_area.configure(state="normal")
            self.text_area.delete("1.0", "end")
            self.text_area.insert("1.0","Bitte gib zusätzliche Informationen ein.")
            self.text_area.configure(state="disabled")
            self.add_window.destroy()
            self.open_add_aircraft()

        elif self.confirm_add_hardpoints == "Error":
            self.text_area.configure(state="normal")
            self.text_area.delete("1.0", "end")
            self.text_area.insert("1.0", "Bitte gib zusätzliche Informationen ein.")
            self.text_area.configure(state="disabled")
            self.add_window.destroy()
            self.open_add_aircraft()

        else:
            self.info_flieger = info_flieger
            self.save_data()
            if self.confirm_add_hardpoints == True:
                self.open_add_hardpoints()

    def save_data(self):
        if self.nationen_entry:
            neue_nation = self.nationen_entry.get().strip()
        neues_flugzeug = self.flugzeug_entry.get().strip()

        if not self.nationen_entry:
            for entry in aircraft_data:
                if entry.name == neues_flugzeug:
                    neue_nation = entry.nation


        if neues_flugzeug:
            # Füge neue Nation hinzu, falls sie noch nicht existiert
            if neue_nation and neue_nation not in self.nationen:
                self.nationen.append(neue_nation)
                self.flugzeuge_pro_nation[neue_nation] = []

            # Füge das neue Flugzeug zur entsprechenden Nation hinzu
                if neue_nation:
                    self.flugzeuge_pro_nation[neue_nation].append(neues_flugzeug)

            existing = False
            for entry in aircraft_data:
                if entry.name == neues_flugzeug:
                    existing = True
                    pass #dann kein append

            if existing == False:
                new_airplane = Class_Structure.Airplane(
                    nation=self.info_flieger[0],
                    name=self.info_flieger[1],
                    battlerating=self.info_flieger[2],
                    plane_type=self.info_flieger[3],
                    turnrate=self.info_flieger[4],
                    climbrate=self.info_flieger[5],
                    speed= self.info_flieger[6],
                    speedheight=self.info_flieger[7],
                    maxheight=self.info_flieger[8]
                )
                aircraft_data.append(new_airplane)
            elif existing == True:
                pass

            # Speichere die neuen Daten in der CSV-Datei
            cw.export_aircraft(filename_aircraft, aircraft_data)
            self.update_parameters()

            # Schließe das Add-Fenster
            self.add_window.destroy()
            self.nationen_combobox.configure(values=self.nationen)  # Aktualisiere die Nationen-ComboBox
            self.text_area.insert("1.0", f"Neue Nation und Flugzeug hinzugefügt: {neue_nation} - {neues_flugzeug}\n")
        else:
            self.text_area.insert("1.0", "Bitte gib ein Flugzeug an.")
#__________________________________________________________________________________________________________________________________________________________
    '''
    def delete_entry(self): #Muss noch für Objekte umgebaut werden
        if self.selected_nation and self.selected_flugzeug:
            # Lösche das Flugzeug aus den Daten
            aircraft_data[:] = [zeile for zeile in aircraft_data if not (
                        zeile['Nation'] == self.selected_nation and zeile['Flugzeug'] == self.selected_flugzeug)]
            self.flugzeuge_pro_nation[self.selected_nation].remove(self.selected_flugzeug)
            self.text_area.insert("1.0",
                                  f"Flugzeug '{self.selected_flugzeug}' aus '{self.selected_nation}' gelöscht.\n")
            cw.export_aircraft(filename_aircraft, aircraft_data)  # Speichere die Änderungen
            self.flugzeuge_combobox.configure(
                values=self.flugzeuge_pro_nation[self.selected_nation])  # Aktualisiere die Combobox
            self.update_parameters()
        else:
            self.text_area.insert("1.0", "Bitte wähle eine Nation und ein Flugzeug zum Löschen aus.")
    '''
#_____________________________________________________________________________________________________________________________________________________________

if __name__ == "__main__":
    app = FlugzeugDatenApp()
    app.mainloop()


'''
### = Brauchen wir noch
- __init__                          #init
- update_parameters                 #DB Listen aktualisieren
- create_widgets                    #gridstruktur
- choose_wiki                       #Waffen oder Flugzeugwiki
- create_widgets_flugzeuge          #UI Für Flugzeugwiki
- create_widgets_waffen             #UI Für Waffenwiki
- nation_ausgewaehlt                #Um die Liste der Flugzeuge zu begrenzen
- armament_type_ausgewaehlt         #Um die Liste der Waffen zu begrenzen
- flugzeug_ausgewaehlt              #Für Flugzeugdaten anzeigen bei drücken von bestätigen
- flugzeug_ausgewaehlt_loeschen     #Fürs löschen eines Flugzeugs bei Drücken von löschen
- waffe_ausgewählt                  #Equivaltent zu Flugzeug eausgewählt
### waffe_ausgewaehlt_loeschen
- zeige_flugzeug_daten              #duh
- zeige_waffen_daten                #duh
- open_add_aircraft                 #Fenster zum hinzufügen von Flugzeugen, hat nur die Abfrage der Nation drin
- open_add_hardpoints
### open_weapon_structure
### open_add_weapon
### open_edit_weapon
### delete_weapon_window
- open_delete_aircraft              #Fenster zum löschen von Flugzeugen und Nationen
- open_edit_aircraft                #Öffnet das Fenster zum editieren, nur mit der Info welches Flugzeug ausgewählt werden soll                 Hi :) o3o 
- open_aircraft_structure           #Struktur für adden und editieren, enthält die Entrys für alle Stats
### open_edit_armament_window
- add_aircraft                      
- edit_aircraft                     #Fenster zum editieren von Flugzeugen
- edit_bestaetigen
- delete_aircraft
- neue_nation_checktask
- bestaetigen
- save_data
- delete_entry                      # Veraltet
'''