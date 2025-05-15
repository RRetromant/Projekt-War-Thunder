import customtkinter as ctk
import csv

# Daten laden (ersetze 'Aircraft.csv' durch deinen Dateipfad)
def lade_csv_daten(dateipfad):
    try:
        with open(dateipfad, 'r', newline='', encoding='utf-8') as datei:
            reader = csv.DictReader(datei)
            daten = list(reader)
            return daten
    except FileNotFoundError:
        print(f"Fehler: Die Datei '{dateipfad}' wurde nicht gefunden.")
        return None
    except Exception as e:
        print(f"Fehler beim Lesen der Datei: {e}")
        return None

# Flugzeugdaten laden
dateipfad = 'Aircraft.csv'  #  Dateipfad
flugzeugdaten = lade_csv_daten(dateipfad) # bleibt drin!!!

if flugzeugdaten is None:
    print("Fehler: Konnte die Flugzeugdaten nicht laden.")
    exit()  # Beende das Programm, wenn die Daten nicht geladen werden konnten

class FlugzeugDatenApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Wiki")
        self.geometry("800x600")  # Fenster größe
        self.grid_columnconfigure(1, weight=1)  # Für das Textfeld
        self.grid_rowconfigure(0, weight=1)  # Für das Hauptfenster

        self.selected_nation = None
        self.selected_flugzeug = None
        self.nationen = sorted(list(set(zeile['Nation'] for zeile in flugzeugdaten)))
        self.flugzeuge_pro_nation = {}
        for nation in self.nationen:
            self.flugzeuge_pro_nation[nation] = sorted(
                list(set(zeile['Flugzeug'] for zeile in flugzeugdaten if zeile['Nation'] == nation)))

        self.create_widgets()

    def create_widgets(self):
        # Linke Seite: Auswahlbereiche
        self.frame_links = ctk.CTkFrame(master=self, width=200)
        self.frame_links.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.nationen_label = ctk.CTkLabel(master=self.frame_links,text="Nation auswählen:")
        self.nationen_label.pack(pady=10)

        self.nationen_combobox = ctk.CTkComboBox(master=self.frame_links, values=self.nationen,command=self.nation_ausgewaehlt)
        self.nationen_combobox.pack(pady=10)

        self.flugzeuge_label = ctk.CTkLabel(master=self.frame_links, text="Flugzeug auswählen:")
        self.flugzeuge_label.pack(pady=10)

        self.flugzeuge_combobox = ctk.CTkComboBox(master=self.frame_links, values=[], state = 'normal', command=self.flugzeug_ausgewaehlt)          #state = normal
        self.flugzeuge_combobox.pack(pady=10)

        self.confirm_button = ctk.CTkButton(master=self.frame_links, text="Bestätigen", command=self.zeige_daten)
        self.confirm_button.pack(pady=20)

        self.add_button = ctk.CTkButton(master=self.frame_links, text="Add Nation/Flugzeug", command=self.open_add_window)
        self.add_button.pack(pady=10)

        self.delete_button = ctk.CTkButton(master=self.frame_links, text="Löschen", command=self.delete_entry)
        self.delete_button.pack(pady=10)
#______________________________________________________________________________________________________________________________Oben: Daten Flugzeug
        self.text_area = ctk.CTkTextbox(master=self, width=400, wrap="word")
        self.text_area.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")
        self.text_area.configure(state="disabled")
#________________________________________________________________________________________________________________________________Unten: Daten Pylon
        self.text_area_pylon = ctk.CTkTextbox(master=self, width=400, wrap="word")
        self.text_area_pylon.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.text_area_pylon.configure(state="disabled")
#___________________________________________________________________________________________________________________________________________________
    def nation_ausgewaehlt(self, nation):
        self.selected_nation = nation
        self.flugzeuge_combobox.configure(values=self.flugzeuge_pro_nation.get(nation, []))
        self.flugzeuge_combobox.set = None  # Setze die Auswahl zurück
        self.selected_flugzeug = None
        self.text_area.delete("1.0", "end")  # Lösche den Text

    def flugzeug_ausgewaehlt(self, flugzeug):
        self.selected_flugzeug = flugzeug

    def zeige_daten(self):
        self.text_area.configure(state="normal") # Normal: Textfeld kann bearbeitet werden
        self.text_area.delete("1.0", "end")  # Lösche den alten Text
        if self.selected_nation and self.selected_flugzeug:
            for zeile in flugzeugdaten:
                if zeile['Nation'] == self.selected_nation and zeile['Flugzeug'] == self.selected_flugzeug:
                    daten_text = "Daten des Flugzeugs:\n"
                    for key, value in zeile.items():
                        daten_text += f"- {key}: {value}\n"
                    self.text_area.insert("1.0", daten_text)
                    self.text_area.configure(state="disabled") # disable : read only
                    return  # Beende die Suche, sobald das Flugzeug gefunden wurde

            self.text_area.insert("1.0", "Flugzeugdaten nicht gefunden.")
        else:
            self.text_area.insert("1.0", "Bitte wähle eine Nation und ein Flugzeug aus.")

    def open_add_window(self):
        self.add_window = ctk.CTkToplevel(self)
        self.add_window.title("Add Nation/Flugzeug")
        self.add_window.geometry("400x500")

        self.nation_entry = ctk.CTkEntry(master=self.add_window, placeholder_text="Neue Nation (optional)")
        self.nation_entry.pack(pady=10)

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

        self.confirm_add_button = ctk.CTkButton(master=self.add_window, text="Confirm", command=self.save_data)
        self.confirm_add_button.pack(pady=20)

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

    def save_data(self):
        neue_nation = self.nation_entry.get().strip()
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
            else:
                # Wenn keine Nation angegeben ist, füge das Flugzeug einfach hinzu (ohne Nation)
                neue_nation = "Unbekannt"  # Setze einen Standardwert für die Nation
                self.flugzeuge_pro_nation[neue_nation] = []

            flugzeugdaten.append({
                'Nation': neue_nation,
                'Flugzeug': neues_flugzeug,
                'BattleRating': battle_rating,
                'Klasse': klasse,
                'Turnrate': turnrate,
                'Steigrate': steigrate,
                'Geschwindigkeit': geschwindigkeit,
                'beiHoehe': bei_hoehe,
                'maxHoehe': max_hoehe
            })

            # Speichere die neuen Daten in der CSV-Datei
            self.save_to_csv()

            # Schließe das Add-Fenster
            self.add_window.destroy()
            self.nationen_combobox.configure(values=self.nationen)  # Aktualisiere die Nationen-ComboBox
            self.text_area.insert("1.0", f"Neue Nation und Flugzeug hinzugefügt: {neue_nation} - {neues_flugzeug}\n")
        else:
            self.text_area.insert("1.0", "Bitte gib ein Flugzeug an.")

    def delete_entry(self):
        if self.selected_nation and self.selected_flugzeug:
            # Lösche das Flugzeug aus den Daten
            flugzeugdaten[:] = [zeile for zeile in flugzeugdaten if not (
                        zeile['Nation'] == self.selected_nation and zeile['Flugzeug'] == self.selected_flugzeug)]
            self.flugzeuge_pro_nation[self.selected_nation].remove(self.selected_flugzeug)
            self.text_area.insert("1.0",
                                  f"Flugzeug '{self.selected_flugzeug}' aus '{self.selected_nation}' gelöscht.\n")
            self.save_to_csv()  # Speichere die Änderungen
            self.flugzeuge_combobox.configure(
                values=self.flugzeuge_pro_nation[self.selected_nation])  # Aktualisiere die Combobox
        else:
            self.text_area.insert("1.0", "Bitte wähle eine Nation und ein Flugzeug zum Löschen aus.")

    def save_to_csv(self):
        try:
            with open(dateipfad, 'w', newline='', encoding='utf-8') as datei:
                fieldnames = ['Nation', 'Flugzeug', 'BattleRating', 'Klasse', 'Turnrate', 'Steigrate',
                              'Geschwindigkeit', 'beiHoehe', 'maxHoehe']
                writer = csv.DictWriter(datei, fieldnames=fieldnames)
                writer.writeheader()
                for zeile in flugzeugdaten:
                    writer.writerow(zeile)
            print("Daten erfolgreich gespeichert.")
        except Exception as e:
            print(f"Fehler beim Speichern der Datei: {e}")



if __name__ == "__main__":
    app = FlugzeugDatenApp()
    app.mainloop()