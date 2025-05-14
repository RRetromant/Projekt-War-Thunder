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

'''
def export_csv(filename, aircraft_list):
    with open(filename, 'w', newline='') as csvfile:
        aircraft_writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for s in aircraft_list:
            values = [str(s.getSchuelerNr()), s.getVorname(), s.getName(),
                      str(s.getAlter())]
            #print(values)
            aircraft_writer.writerow(values)
'''

test = import_Aircraft("Aircraft.csv")