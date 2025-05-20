import customtkinter as ctk
import CSVWorker as cw
import Class_Structure

'''
___Inhaltsverzeichnis___

__init__                        Konstruktor
update_parameters			    Aktualisiert Listen
-----------------------------------------------------------------------------------------------------------
create_widgets				    gridstruktur
choose_wiki				        Waffen oder Flugzeugwiki
create_widgets_flugzeuge		UI für Flugzeugwiki
create_widgets_waffen			UI für Waffenwiki
-----------------------------------------------------------------------------------------------------------
nation_ausgewaehlt			    speichert gewählte Nation, baut eine Liste von Fliegern pro Nation
armament_type_ausgewaehlt		speichert gewählten Waffentyp, baut eine Liste von Waffen pro Typ
flugzeug_ausgewaehlt			Gewähltes Flugzeug zwischenspeichern
flugzeug_ausgewaehlt_loeschen   Gewähltes Flugzeug zum löschen zwischenspeichern //Sicherung
waffe_ausgewaehlt			    Gewählte Waffe zwischenspeichern
waffe_ausgewaehlt_loeschen		Gewählte Waffe zum löschen zwischenspeichern //Sicherung
zeige_flugzeug_daten			Sammelt Flugzeugdaten und gibt sie in test_area aus
zeige_waffen_daten			    Sammelt Waffendaten und gibt sie in test_area aus
-----------------------------------------------------------------------------------------------------------
open_add_aircraft			    Baut neues Fenster, fragt ob es ne neue Nation gibt und gibt an
					            open_aircraft_structure weiter
open_edit_aircraft			    Baut neues Fenster, fragt nach zu bearbeitendem Flugzeug
open_delete_aircraft			Baut neues Fenster, fragt nach zu löschendem Objekt, und gibt an
					            delete_aircraft weiter
open_aircraft_structure			Beinhaltet die Eingabefenster für Flugzeuge und Confirm-Button
-----------------------------------------------------------------------------------------------------------
neue_nation_checktask			Ändert den Nationen-Entry und gibt an add-aircraft weiter
add_aircraft				    Ruft die Struktur auf und bearbeitet den Confirm-Button
edit_aircraft				    bearbeitet den Confirm-Button und füllt die Felder mit dem zu 
					            bearbeitenden Flugzeug aus
delete_aircraft				    Löscht den Eintrag eines Flugzeugs. Danach export und Update.
bestaetigen				        Prüft ob alle Felder gefüllt sind, und gibt an save_new_aircraft weiter
edit_bestaetigen			    Prüft ob alle Felder gefüllt sind, und ändert den Eintrag in 
					            aircraft_data. Danach export und Update.
save_new_aircraft			    Checkt, ob das Flugzeug und die Nation neu ist, und erstellt ein neues 
					            Airplane-Objekt. Danach speichern, export und update
-----------------------------------------------------------------------------------------------------------	         
open_add_weapon				    Baut neues Fenster, gibt an open_weapon_structure weiter
open_edit_weapon                braucht zwei Abfragen: type und Name.
open_delete_weapon			    braucht zwei Abfragen: type und Name.
open_weapon_structure			Fragt nach Waffentyp, gibt dann an open_weapon_rest weiter
open_weapon_rest                Zeigt je nach Waffentyp alle Fenster an
-----------------------------------------------------------------------------------------------------------
add_weapon                      Fügt Waffen hinzu
edit_weapon                     Bestehende Waffen editierbar
delete_weapon                   Waffen können gelöscht werden mit sicheheitsabfrage
get_weapon_class                Checkt, welche Klasse die Waffe ist, und bei die Infoliste entsprechend für speichern, editieren usw.
get_weapon_class_translate
Weapon_bestaetigen              
edit_weapon_bestaetigen         
save_new_weapon                 
'''

# Flugzeugdaten laden
filename_aircraft = 'Aircraft.csv'  #  Dateipfad
filename_armament = 'Armament.csv'
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
        self.armament = sorted({arm.name for arm in armament_data})

        self.weapon_types = sorted({weapon.armament_type for weapon in armament_data})
        self.waffen_pro_type = {
            type: sorted({weapon.name for weapon in armament_data if weapon.armament_type == type})
            for type in self.weapon_types
        }

    #Aufbau des Hauptfensters
    # __________________________________________________________________________________________________________________________________________________________________________________________________
    def create_widgets(self):
        # Linke Seite: Auswahlbereiche
        self.frame_links = ctk.CTkFrame(master=self, width=200)
        #Reihe 0 (ganz links), Spalte 0 (ganz oben), Soll über beide Reihen gehen
        self.frame_links.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.nationen_label = ctk.CTkLabel(master=self.frame_links,text="Wiki auswählen:")
        self.nationen_label.pack(pady=10)

        self.wiki_checker = ctk.CTkOptionMenu(master=self.frame_links, values=['Flugzeuge', 'Waffen'], state='normal',command=self.choose_wiki)  # state = normal
        self.wiki_checker.pack(pady=10)
        self.wiki_checker.set('')

    def choose_wiki(self, auswahl, override = False):
        #if hasattr(self, 'nationen_entry'):
        for widget in self.frame_links.winfo_children():
            widget.destroy()
        try:
            self.text_area.destroy()                            #Löscht das Textfeld (Falls vorhanden)
        except:
            pass

        self.nationen_label = ctk.CTkLabel(master=self.frame_links,text="Wiki auswählen:")
        self.nationen_label.pack(pady=10)

        self.wiki_checker = ctk.CTkOptionMenu(master=self.frame_links, values=['Flugzeuge', 'Waffen'], state='normal',command=self.choose_wiki)  # state = normal
        self.wiki_checker.pack(pady=10)
        self.wiki_checker.set('')

        if auswahl == "Flugzeuge":
            self.create_widgets_flugzeuge()

        elif auswahl == "Waffen":
            self.create_widgets_waffen()

    def create_widgets_flugzeuge(self):
        font_size = 30#Schriftgröße (Textfeld)

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

    #Daten Output ______________________________________________________________________________________________________________________________
        self.text_area = ctk.CTkTextbox(master=self, width=400,font=("", font_size),wrap="word")
        self.text_area.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.text_area.configure(state="disabled")  # Damit das Textfeld von anfang an nicht bearbeitet werden kann
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

        self.add_button_waffen = ctk.CTkButton(master=self.frame_links, text="Add Armament",command=self.open_add_weapon)
        self.add_button_waffen.pack(pady=10)
        #self.add_button_waffen.configure(state="disabled")

        self.edit_armament_button = ctk.CTkButton(master=self.frame_links, text="Edit Armament",command=self.open_edit_weapon)
        self.edit_armament_button.pack(pady=10)
        #self.edit_armament_button.configure(state="disabled")

        self.delete_button = ctk.CTkButton(master=self.frame_links, text="Löschen", command=self.open_delete_weapon)
        self.delete_button.pack(pady=10)
        #self.delete_button.configure(state="disabled")
        # Oben: Daten Flugzeug______________________________________________________________________________________________________________________________
        self.text_area = ctk.CTkTextbox(master=self, width=400, wrap="word")
        self.text_area.grid(row=0, column=1,  padx=20, pady=20, sticky="nsew")
        self.text_area.configure(state="disabled")  # Damit das Textfeld von anfang an nicht bearbeitet werden kann

    #Auswählen und Anzeigen von Daten
    # _____________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________
    def nation_ausgewaehlt(self, nation):
        self.selected_nation = nation
        self.flugzeuge_combobox.configure(values=self.flugzeuge_pro_nation.get(nation, [])) #(Output)Flugzeuge der ausgewählten nation                             #Dropdown menü (Nation)     # Setze die Auswahl zurück
        self.selected_flugzeug = None
        self.text_area.delete("1.0", "end")      # Lösche den Text

    def armament_type_ausgewaehlt(self, type):
        self.selected_weapon_type = type
        self.waffen_option.configure(values=self.waffen_pro_type.get(type, []))  # Dropdown menü (Nation)     # Setze die Auswahl zurück
        self.text_area.delete("1.0", "end")  # Lösche den Text

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

    # __________________________________________________________________________________________________________________________________________________________________________________________________
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

    #Flugzeugwiki Editierfenster
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
        self.confirm_add_button.configure (command=self.edit_bestaetigen)

    def open_delete_aircraft(self):

        self.delete_window = ctk.CTkToplevel(self)
        self.delete_window.title("Löschfenster")
        self.delete_window.geometry("360x400")

        self.delete_abfrage = ctk.CTkLabel(master=self.delete_window,text = ("Bitte wählen sie einen Flugzeug aus: "))
        self.delete_abfrage.pack(pady=10)

        self.delete_flugzeug = ctk.CTkOptionMenu(master=self.delete_window, values=self.aircraft, state='normal',command=self.flugzeug_ausgewaehlt_loeschen)  # state = normal
        self.delete_flugzeug.pack(pady=10)
        self.delete_flugzeug.set('')

        self.loeschen_button = ctk.CTkButton(master=self.delete_window, text="Löschen", command=self.delete_aircraft)
        self.loeschen_button.pack(pady=10)

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

        self.confirm_add_button = ctk.CTkButton(master=self.add_window, text="Confirm", command=self.bestaetigen)
        self.confirm_add_button.pack(pady=20)

# Flugzeugwiki Editierablauf
# _________________________________________________________________________________________________________________________________________________________
    def neue_nation_checktask(self, auswahl):  # Damit der Button live gecheckt wird
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

    def add_aircraft(self):
        self.open_aircraft_structure()
        self.confirm_add_button.configure(command=self.bestaetigen)
        self.confirm_add_button.pack(pady=20)

    def edit_aircraft(self, auswahl):
        self.flugzeug_ausgewaehlt(auswahl)
        for entry in aircraft_data:
            if self.selected_flugzeug == entry.name:
                self.flugzeug_entry.delete(0, 'end')
                self.flugzeug_entry.insert(0, entry.name)
                self.battle_rating_entry.delete(0, 'end')
                self.battle_rating_entry.insert(0, entry.battlerating)
                self.klasse_entry.delete(0, 'end')
                self.klasse_entry.insert(0, entry.plane_type)
                self.turnrate_entry.delete(0, 'end')
                self.turnrate_entry.insert(0, entry.turnrate)
                self.steigrate_entry.delete(0, 'end')
                self.steigrate_entry.insert(0, entry.climbrate)
                self.geschwindigkeit_entry.delete(0, 'end')
                self.geschwindigkeit_entry.insert(0, entry.speed)
                self.bei_hoehe_entry.delete(0, 'end')
                self.bei_hoehe_entry.insert(0, entry.speedheight)
                self.max_hoehe_entry.delete(0, 'end')
                self.max_hoehe_entry.insert(0, entry.maxheight)

    def delete_aircraft(self):
        for entry in aircraft_data:
            if (entry.name == self.flugzeug_zu_loeschen):
                aircraft_data.remove(entry)
                self.text_area.configure(state="normal")
                self.text_area.delete("1.0", "end")
                self.text_area.insert("1.0", "Flugzeug gelöscht!.")
                self.text_area.configure(state="disabled")
                self.delete_window.destroy()
        cw.export_aircraft(filename_aircraft, aircraft_data)
        self.update_parameters()
        self.choose_wiki("Flugzeuge")

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
        if not info_flieger[0]:  # Eintrag Nation ist leer
            self.text_area.configure(state="normal")
            self.text_area.delete("1.0", "end")
            self.text_area.insert("1.0", "Bitte gib den Namen der Nation ein.")
            self.text_area.configure(state="disabled")
            self.add_window.destroy()
            self.open_add_aircraft()

        elif info_flieger[0] == "Nation auswählen":  # Eintrag Nation ist leer
            self.text_area.configure(state="normal")
            self.text_area.delete("1.0", "end")
            self.text_area.insert("1.0", "Bitte gib den Namen der Nation ein.")
            self.text_area.configure(state="disabled")
            self.add_window.destroy()
            self.open_add_aircraft()

        elif any(eintrag == '' for eintrag in info_flieger[1:]):
            self.text_area.configure(state="normal")
            self.text_area.delete("1.0", "end")
            self.text_area.insert("1.0", "Bitte gib zusätzliche Informationen ein.")
            self.text_area.configure(state="disabled")
            self.add_window.destroy()
            self.open_add_aircraft()

        else:
            self.info_flieger = info_flieger
            self.save_new_aircraft()

    def edit_bestaetigen(self):
        info_flieger = [
            # self.nationen_entry.get(),
            self.flugzeug_entry.get(),
            self.battle_rating_entry.get(),
            self.klasse_entry.get(),
            self.turnrate_entry.get(),
            self.steigrate_entry.get(),
            self.geschwindigkeit_entry.get(),
            self.bei_hoehe_entry.get(),
            self.max_hoehe_entry.get()
        ]
        if not info_flieger[0]:  # Eintrag Nation ist leer
            self.text_area.configure(state="normal")
            self.text_area.delete("1.0", "end")
            self.text_area.insert("1.0", "Bitte gib den Namen der Nation ein.")
            self.text_area.configure(state="disabled")
            # self.open_aircraft_structure.destroy()

        elif info_flieger[0] == "Nation auswählen":  # Eintrag Nation ist leer
            self.text_area.configure(state="normal")
            self.text_area.delete("1.0", "end")
            self.text_area.insert("1.0", "Bitte gib den Namen der Nation ein.")
            self.text_area.configure(state="disabled")
            # self.open_aircraft_structure.destroy()

        elif any(eintrag == '' for eintrag in info_flieger[1:]):
            self.text_area.configure(state="normal")
            self.text_area.delete("1.0", "end")
            self.text_area.insert("1.0", "Bitte gib zusätzliche Informationen ein.")
            self.text_area.configure(state="disabled")
            # self.open_aircraft_structure.destroy()
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

    def save_new_aircraft(self):
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
                    pass

            if existing == False:
                new_airplane = Class_Structure.Airplane(
                    nation=self.info_flieger[0],
                    name=self.info_flieger[1],
                    battlerating=self.info_flieger[2],
                    plane_type=self.info_flieger[3],
                    turnrate=self.info_flieger[4],
                    climbrate=self.info_flieger[5],
                    speed=self.info_flieger[6],
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
            self.text_area.insert("1.0",
                                  f"Neue Nation und Flugzeug hinzugefügt: {neue_nation} - {neues_flugzeug}\n")
        else:
            self.text_area.insert("1.0", "Bitte gib ein Flugzeug an.")

#Waffenwiki Editierfenster
# ___________________________________________________________________________________________________________________________________________________
    def open_add_weapon(self):
        self.weapon_window = ctk.CTkToplevel(self)
        self.weapon_window.title("Waffen Fenster")
        self.weapon_window.geometry("400x650")
        self.open_weapon_structure()

    def open_edit_weapon(self):
        self.weapon_window = ctk.CTkToplevel(self)
        self.weapon_window.title("Waffen Fenster")
        self.weapon_window.geometry("400x650")
        print(self.selected_weapon_type)
        print(self.selected_waffe)
        self.open_weapon_rest()
        self.edit_weapon()

    def open_delete_weapon(self):
        pass

    def open_weapon_structure(self, edit_window=False):

        self.weapon_entry = ctk.CTkLabel(master=self.weapon_window, text="Waffentyp:")
        self.weapon_entry.pack(pady=5)

        self.weapon_type_entry = ctk.CTkOptionMenu(master=self.weapon_window, values=self.weapon_types,
                                                   command=self.clear_weapon_structure)
        self.weapon_type_entry.pack(pady=5)

    def clear_weapon_structure(self, auswahl):
        self.armament_type_ausgewaehlt(auswahl)
        print("Attributänderung")
        try:
            self.weapon_entry.destroy()
            self.projectile_mass_entry.destroy()
        except:
            pass

        try:
            self.explo_type_entry.destroy()
            self.explosive_mass_entry.destroy()
            self.TNT_equivalent_entry.destroy()
        except:
            pass

        try:
            self.guidance_entry.destroy()
            self.missile_guidance_time_entry.destroy()
        except:
            pass

        try:
            self.launch_range_entry.destroy()
            self.max_speed_entry.destroy()
        except:
            pass

        try:
            self.aspect_entry.destroy()
            self.lockrange_entry.destroy()
            self.lockrange_rear_entry.destroy()
            self.max_g_entry.destroy()
        except:
            pass

        try:
            self.confirm_add_button.destroy()
        except:
            pass

        self.open_weapon_rest()

    def open_weapon_rest(self):

        self.weapon_entry = ctk.CTkEntry(master=self.weapon_window, placeholder_text="Neue Waffe")
        self.weapon_entry.pack(pady=10)

        self.projectile_mass_entry = ctk.CTkEntry(master=self.weapon_window, placeholder_text="Projectile Mass")
        self.projectile_mass_entry.pack(pady=5)

        if self.selected_weapon_type in ["dumb bombs","retarded bombs", "dumb rockets" ,"guided-bombs", "Air-to-Ground", "Air-to-Air"]:

            self.explo_type_entry = ctk.CTkEntry(master=self.weapon_window, placeholder_text="Explosive Type")
            self.explo_type_entry.pack(pady=5)

            self.explosive_mass_entry = ctk.CTkEntry(master=self.weapon_window, placeholder_text="Explosive Mass")
            self.explosive_mass_entry.pack(pady=5)

            self.TNT_equivalent_entry = ctk.CTkEntry(master=self.weapon_window, placeholder_text="TNT equivalent")
            self.TNT_equivalent_entry.pack(pady=5)

        if self.selected_weapon_type in ["guided-bombs", "Air-to-Ground", "Air-to-Air"]:
            self.guidance_entry = ctk.CTkEntry(master=self.weapon_window, placeholder_text="Guidance")
            self.guidance_entry.pack(pady=5)

            self.missile_guidance_time_entry = ctk.CTkEntry(master=self.weapon_window, placeholder_text="Missile Guidance Time")
            self.missile_guidance_time_entry.pack(pady=5)

        if self.selected_weapon_type in ["Air-to-Ground", "Air-to-Air"]:
            self.launch_range_entry = ctk.CTkEntry(master=self.weapon_window,
                                                                placeholder_text="Launch Range")
            self.launch_range_entry.pack(pady=5)

            self.max_speed_entry = ctk.CTkEntry(master=self.weapon_window,
                                                                placeholder_text="Maximum Speed")
            self.max_speed_entry.pack(pady=5)

        if self.selected_weapon_type in ["Air-to-Air"]:
            self.aspect_entry = ctk.CTkEntry(master=self.weapon_window, placeholder_text="Aspect")
            self.aspect_entry.pack(pady=5)

            self.lockrange_entry = ctk.CTkEntry(master=self.weapon_window, placeholder_text="Lock-Reichweite")
            self.lockrange_entry.pack(pady=5)

            self.lockrange_rear_entry = ctk.CTkEntry(master=self.weapon_window, placeholder_text="Lock-Range von hinten")
            self.lockrange_rear_entry.pack(pady=5)

            self.max_g_entry = ctk.CTkEntry(master=self.weapon_window, placeholder_text="Maximale G Belastung")
            self.max_g_entry.pack(pady=5)

        self.confirm_add_button = ctk.CTkButton(master=self.weapon_window,text="Confirm", command=self.weapon_bestaetigen)
        self.confirm_add_button.pack(pady=20)

#Waffenwiki Editierablauf
#__________________________________________________________________________________________________________________________________________________________
    def add_weapon(self):
        pass

    def edit_weapon(self):
        for entry in armament_data:
            if self.selected_waffe == entry.name:

                #self.armament_type_entry.delete(0, 'end')
                #self.armament_type_entry.insert(0, entry.armament_type)

                try:
                    #self.weapon_entry.delete(0, 'end')
                    #self.weapon_entry.insert(0, entry.name)
                    self.projectile_mass_entry.delete(0, 'end')
                    self.projectile_mass_entry.insert(0, entry.projectile_mass)
                except:
                    pass

                try:
                    self.explo_type_entry.delete(0, 'end')
                    self.explo_type_entry.insert(0, entry.explosive_type)
                    self.explosive_mass_entry.delete(0, 'end')
                    self.explosive_mass_entry.insert(0, entry.explosive_mass)
                    self.TNT_equivalent_entry.delete(0, 'end')
                    self.TNT_equivalent_entry.insert(0, entry.TNT_equivalent)
                except:
                    pass

                try:
                    self.guidance_entry.delete(0, 'end')
                    self.guidance_entry.insert(0, entry.guidance)
                    self.missile_guidance_time_entry.delete(0, 'end')
                    self.missile_guidance_time_entry.insert(0, entry.missile_guidance_time)        # entry
                except:
                    pass

                try:
                    self.launch_range_entry.delete(0, 'end')
                    self.launch_range_entry.insert(0, entry.launch_range)
                    self.max_speed_entry.delete(0, 'end')
                    self.max_speed_entry.insert(0, entry.maxspeed)
                except:
                    pass

                try:
                    self.aspect_entry.delete(0, 'end')
                    self.aspect_entry.insert(0, entry.aspect)
                    self.lockrange_entry.delete(0, 'end')
                    self.lockrange_entry.insert(0, entry.lock_range)
                    self.lockrange_rear_entry.delete(0, 'end')
                    self.lockrange_rear_entry.insert(0, entry.lock_range_rear)
                    self.max_g_entry.delete(0, 'end')
                    self.max_g_entry.insert(0, entry.maxg_overload)
                except:
                    pass

    def delete_weapon(self):
        pass

    def get_weapon_class(self, show_all= False): # =42
        waffen_info_entries = [
            "weapon_entry",
            "weapon_type_entry",
            "projectile_mass_entry"
        ]
        if self.selected_weapon_type in ("dumb bombs","retarded bombs", "dumb rockets" ,"guided-bombs", "Air-to-Ground", "Air-to-Air") or show_all:
            waffen_info_entries.append("explo_type_entry")
            waffen_info_entries.append("explosive_mass_entry")
            waffen_info_entries.append("TNT_equivalent_entry")
        if self.selected_weapon_type in ("guided-bombs", "Air-to-Ground", "Air-to-Air") or show_all:
            waffen_info_entries.append("guidance_entry")
            waffen_info_entries.append("missile_guidance_time_entry")
        if self.selected_weapon_type in ("Air-to-Ground", "Air-to-Air") or show_all:
            waffen_info_entries.append("launch_range_entry")
            waffen_info_entries.append("max_speed_entry")
        if self.selected_weapon_type in ("Air-to-Air") or show_all:
            waffen_info_entries.append("aspect_entry")
            waffen_info_entries.append("lockrange_entry")
            waffen_info_entries.append("lockrange_rear_entry")
            waffen_info_entries.append("max_g_entry")

        return waffen_info_entries

    def get_weapon_class_translate(self, info_waffe):
        for fromKey, toKey in [("weapon_entry", "Name"),    #Übersetzer, damit die Werte CSVWorker entsprechen
                               ("weapon_type_entry", "Type"),
                               ("projectile_mass_entry", "Projectile-Masse"),
                               ("explo_type_entry", "Explosive-Type"),
                               ("explosive_mass_entry", "Explosive-Mass"),
                               ("TNT_equivalent_entry", "TNT-equivalent"),
                               ("guidance_entry", "Guidance"),
                               ("missile_guidance_time_entry", "Missile-guidance-time"),
                               ("launch_range_entry", "Launch-range"),
                               ("max_speed_entry", "Maximum-speed"),
                               ("aspect_entry", "Aspect"),
                               ("lockrange_entry", "Lock-range-in-all-aspect"),
                               ("lockrange_rear_entry", "Lock-range-in-rear-aspect"),
                               ("max_g_entry", "Maximum-Overload")]:
            if fromKey in info_waffe:
                info_waffe[toKey] = info_waffe.pop(fromKey)

    def weapon_bestaetigen(self):

        waffen_info_entries = self.get_weapon_class()

        info_waffe = [
            getattr(self, name).get() if hasattr(self, name) else ''
            for name in waffen_info_entries
        ]

        if any(eintrag == '' for eintrag in info_waffe):
            print(info_waffe)
            self.text_area.configure(state="normal")
            self.text_area.delete("1.0", "end")
            self.text_area.insert("1.0", "Bitte gib zusätzliche Informationen ein.")
            self.text_area.configure(state="disabled")
            self.weapon_window.destroy()
            self.open_add_weapon()

        else:
            self.save_new_weapon()

    def edit_weapon_bestaetigen(self):
        waffen_info_entries = self.get_weapon_class()

        info_waffe = [
            getattr(self, name).get() if hasattr(self, name) else ''
            for name in waffen_info_entries
        ]
        waffen_info_entries = self.get_weapon_class()
        print("saving new weapon")
        info_waffe = {}
        for waffe_info_entry in waffen_info_entries:
            info_waffe[waffe_info_entry] = getattr(self, waffe_info_entry).get() if hasattr(self,
                                                                                            waffe_info_entry) else ''
        print(info_waffe)

        self.get_weapon_class_translate(info_waffe)

        edited_weapon = self.selected_waffe

        for entry in armament_data:
            if entry.name == edited_weapon:
                cw.edit_armament(entry)


    def save_new_weapon(self):
        waffen_info_entries = self.get_weapon_class()
        print("saving new weapon")
        info_waffe = {}
        for waffe_info_entry in waffen_info_entries:
            info_waffe[waffe_info_entry] = getattr(self, waffe_info_entry).get() if hasattr(self, waffe_info_entry) else ''
        print(info_waffe)

        self.get_weapon_class_translate(info_waffe)

        new_weapon = info_waffe["Name"]
        existing = False
        for entry in armament_data:
            if entry.name == new_weapon:
                existing = True
                pass

        if not existing:
            new_entry = cw.add_armament(info_waffe)
            print(new_entry)
            armament_data.append(new_entry)
            cw.export_armaments("Armament.csv", armament_data)
        elif existing:
            pass

        self.weapon_window.destroy()
        self.update_parameters()

#Programm Mainloop
#__________________________________________________________________________________________________________________________________________________________
if __name__ == "__main__":
    app = FlugzeugDatenApp()
    app.mainloop()