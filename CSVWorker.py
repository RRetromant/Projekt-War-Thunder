import csv
import Class_Structure


def import_Aircraft(filename):
    aircraft_list = []
    with open(filename) as csvfile:
        aircraft_reader = csv.DictReader(csvfile, delimiter=',')
        for row in aircraft_reader:
            aircraft= Class_Structure.Airplane(
                nation=row['Nation'],
                name=row['Flugzeug'],
                battlerating=row['BattleRating'],
                plane_type=row['Klasse'],
                turnrate=row['Turnrate'],
                climbrate=row['Steigrate'],
                speed=row['Geschwindigkeit'],
                speedheight=row['beiHoehe'],
                maxheight=row['maxHoehe']
            )
            aircraft_list.append(aircraft)

    return aircraft_list



#Wird hier konserviert, statt Objekten nutzt man hier eine riesige Liste.
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

test = lade_csv_daten()
print (test[0])
'''




'''
def export_Aircraft(filename, aircraft_list):  Noch in Arbeit
    with open(filename, 'w', newline='') as csvfile:
        aircraft_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for s in aircraft_list:
            values = [str(s.getSchuelerNr()), s.getVorname(), s.getName(),
                      str(s.getAlter())]
            #print(values)
            aircraft_writer.writerow(values)
'''

#Kann nützlich sein, um die Nationen anzeigen zu lassen
'''
test = import_Aircraft("Aircraft.csv")
testlist = set()
for i in test:
    testlist.add(i.nation)

print(testlist)
'''