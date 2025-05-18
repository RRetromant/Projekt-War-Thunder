from symbol import parameters

import customtkinter as ctk
#import tkintertable as tkt #Weiss noch nicht ob das mit ctk läuft
import csv


import CSVWorker as cw
import Class_Structure

#veraltet
'''
def lade_csv_daten():
    try:
        with open("Aircraft.csv", 'r', newline='', encoding='utf-8') as datei:
            reader = csv.DictReader(datei)
            daten = list(reader)
            return daten
    except FileNotFoundError:
        print(f"Fehler: Die Datei Aircraft.csv wurde nicht gefunden.")
        return None
    except Exception as e:
        print(f"Fehler beim Lesen der Datei: {e}")
        return None
'''

# Flugzeugdaten laden
filename_aircraft = 'Aircraft.csv'  #  Dateipfad
filename_armament = 'Armament.csv'
filename_hardpoint_selected = '' #ändert sich im Laufe des Programms
filename_hardpoint = f'f{filename_hardpoint_selected}_Hardpoints.csv' #damit es flexibel ist
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
        if hasattr(self, 'nationen_entry'):
            pass #Dann clear bitte alle Widgets
        if auswahl == "Flugzeuge":
            self.create_widgets_flugzeuge()
        elif auswahl == "Waffen":
            self.create_widgets_waffen()


    def create_widgets_flugzeuge(self):

        self.nationen_label = ctk.CTkLabel(master=self.frame_links, text="Nation auswählen:")
        self.nationen_label.pack(pady=10)

        self.nationen_combobox = ctk.CTkOptionMenu(master=self.frame_links, values=self.nationen,
                                                   command=self.nation_ausgewaehlt)
        self.nationen_combobox.pack(pady=10)
        self.nationen_combobox.set('')

        self.flugzeuge_label = ctk.CTkLabel(master=self.frame_links, text="Flugzeug auswählen:")
        self.flugzeuge_label.pack(pady=10)

        self.flugzeuge_combobox = ctk.CTkOptionMenu(master=self.frame_links, values=[], state='normal',
                                                    command=self.flugzeug_ausgewaehlt)  # state = normal
        self.flugzeuge_combobox.pack(pady=10)
        self.flugzeuge_combobox.set('')

        self.confirm_button = ctk.CTkButton(master=self.frame_links, text="Bestätigen", command=self.zeige_flugzeug_daten)
        self.confirm_button.pack(pady=20)

        self.add_button = ctk.CTkButton(master=self.frame_links, text="Add Nation/Flugzeug",
                                        command=self.open_add_aircraft)
        self.add_button.pack(pady=10)

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

        self.weapon_type_option = ctk.CTkOptionMenu(master=self.frame_links, values=self.weapon_types, state='normal',
                                                    command=self.armament_type_ausgewaehlt)  # state = normal
        self.weapon_type_option.pack(pady=10)
        self.weapon_type_option.set('')

        self.flugzeuge_label = ctk.CTkLabel(master=self.frame_links, text="Waffe auswählen:")
        self.flugzeuge_label.pack(pady=10)

        self.waffen_option = ctk.CTkOptionMenu(master=self.frame_links, values=[], state='normal',
                                                    command=self.waffe_ausgewählt)  # state = normal
        self.waffen_option.pack(pady=10)
        self.waffen_option.set('')

        self.confirm_button = ctk.CTkButton(master=self.frame_links, text="Bestätigen", command=self.zeige_waffen_daten)
        self.confirm_button.pack(pady=20)

        self.add_button = ctk.CTkButton(master=self.frame_links, text="Add Armament",
                                        command=self.open_add_aircraft)
        self.add_button.pack(pady=10)

        self.edit_button = ctk.CTkButton(master=self.frame_links, text="Edit Armament",
                                         command=self.open_edit_aircraft)
        self.edit_button.pack(pady=10)

        self.delete_button = ctk.CTkButton(master=self.frame_links, text="Löschen", command=self.open_delete_aircraft)
        self.delete_button.pack(pady=10)

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
        self.add_window.geometry("400x600")

        self.nationen_checklabel = ctk.CTkLabel(master=self.add_window, text="Ist es eine neue Nation?:")
        self.nationen_checklabel.pack(pady=10)

        self.neue_nation_checker = ctk.CTkOptionMenu(master=self.add_window,values=("ja", "nein"),command=self.neue_nation_checktask)

        self.neue_nation_checker.pack(pady=10)
        self.neue_nation_checker.set('Bitte auswählen')

    def open_weapon_structure(self):
        pass

    def open_add_weapon(self):
        pass

    def open_edit_weapon(self):
        pass

    def delete_weapon_window(self):
        pass
#________________________________________________________________________________________________________________________________________________________
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

    def edit_aircraft(self):
        self.open_aircraft_structure()
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
            self.open_aircraft_structure.destroy()

        elif info_flieger[0] == "Nation auswählen": #Eintrag Nation ist leer
            self.text_area.configure(state="normal")
            self.text_area.delete("1.0", "end")
            self.text_area.insert("1.0", "Bitte gib den Namen der Nation ein.")
            self.text_area.configure(state="disabled")
            self.open_aircraft_structure.destroy()

        elif any(eintrag == '' for eintrag in info_flieger[1:]):
            self.text_area.configure(state="normal")
            self.text_area.delete("1.0", "end")
            self.text_area.insert("1.0","Bitte gib zusätzliche Informationen ein.")
            self.text_area.configure(state="disabled")
            self.open_aircraft_structure.destroy()
        else:
            self.save_data()

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
    '''' 
            # Dropdown-Menü für bestehende Nationen
            self.nationen = self.flugzeugdaten()
            self.selected_nation = ctk.StringVar(value=self.nationen[0] if self.nationen else "Keine Nationen verfügbar")

            self.nation_dropdown = ctk.CTkOptionMenu(
                master=self.add_window,
                variable=self.selected_nation,
                values=self.nationen + ["Neue Nation hinzufügen"],
                command=self.on_nation_select
            )

            self.nation_dropdown.pack(pady=10)
    '''''
    def bestaetigen(self):
        """Verarbeitet die Eingabe und fügt die Nation hinzu oder zeigt einen Fehler an."""
        nation = self.nationen_entry.get()
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
        else:
            self.save_data()

    def save_data(self):
        neue_nation = self.nationen_entry.get().strip()
        neues_flugzeug = self.flugzeug_entry.get().strip()
        # Werte für das neue Flugzeug
        battle_rating = self.battle_rating_entry.get().strip()
        klasse = self.klasse_entry.get().strip()
        turnrate = self.turnrate_entry.get().strip()
        steigrate = self.steigrate_entry.get().strip()
        geschwindigkeit = self.geschwindigkeit_entry.get().strip()
        bei_hoehe = self.bei_hoehe_entry.get().strip()
        max_hoehe = self.max_hoehe_entry.get().strip()

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
                    nation=neue_nation,
                    name=neues_flugzeug,
                    battlerating=battle_rating,
                    plane_type=klasse,
                    turnrate=turnrate,
                    climbrate=steigrate,
                    speed=geschwindigkeit,
                    speedheight=bei_hoehe,
                    maxheight=max_hoehe
                )
                aircraft_data.append(new_airplane)
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
    def delete_entry(self): #Muss noch für Objekte umgebaut werden
        if self.selected_nation and self.selected_flugzeug:
            # Lösche das Flugzeug aus den Daten
            aircraft_data[:] = [zeile for zeile in aircraft_data if not (
                        zeile['Nation'] == self.selected_nation and zeile['Flugzeug'] == self.selected_flugzeug)]
            self.flugzeuge_pro_nation[self.selected_nation].remove(self.selected_flugzeug)
            self.text_area.insert("1.0",
                                  f"Flugzeug '{self.selected_flugzeug}' aus '{self.selected_nation}' gelöscht.\n")
            cw.export_aircraft(filename, aircraft_data)  # Speichere die Änderungen
            self.flugzeuge_combobox.configure(
                values=self.flugzeuge_pro_nation[self.selected_nation])  # Aktualisiere die Combobox
            self.update_parameters()
        else:
            self.text_area.insert("1.0", "Bitte wähle eine Nation und ein Flugzeug zum Löschen aus.")
#__________________________________________________________________________________________________________________________________________________________
#Der Part wurde ersetzt durch cw.export_Aircraft
'''
    def save_to_csv(self): #Muss noch für Objekte umgebaut werden
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as datei:
                fieldnames = ['Nation', 'Flugzeug', 'BattleRating', 'Klasse', 'Turnrate', 'Steigrate',
                              'Geschwindigkeit', 'beiHoehe', 'maxHoehe']
                writer = csv.DictWriter(datei, fieldnames=fieldnames)
                writer.writeheader()
                for zeile in aircraft_data:
                    writer.writerow(zeile)
            print("Daten erfolgreich gespeichert.")
        except Exception as e:
            print(f"Fehler beim Speichern der Datei: {e}")'''
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
- zeige_flugzeug_daten #duh
- zeige_waffen_daten    #duh
- open_add_aircraft                 #Fenster zum hinzufügen von Flugzeugen, hat nur die Abfrage der Nation drin
### open_weapon_structure
### open_add_weapon
### open_edit_weapon
### delete_weapon_window
- open_delete_aircraft              #Fenster zum löschen von Flugzeugen und Nationen
- open_edit_aircraft                #Fenster zum editieren von Flugzeugen                 Hi :) o3o 
- open_aircraft_structure           #Struktur für adden und editieren, enthält die Entrys
- open_edit_armament_window
- add_aircraft
- edit_aircraft
- edit_bestaetigen
- delete_aircraft
- neue_nation_checktask
- bestaetigen
- save_data
'''