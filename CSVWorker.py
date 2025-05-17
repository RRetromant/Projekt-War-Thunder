import csv
import Class_Structure


def import_aircraft(filename):
    aircraft_list = []
    with open(filename) as csvfile:
        aircraft_reader = csv.DictReader(csvfile, delimiter=',')
        for row in aircraft_reader:
            aircraft = Class_Structure.Airplane(
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


def export_aircraft(filename, aircraft_list):
    with open(filename, 'w', newline='') as csvfile:
        aircraft_writer = csv.writer(csvfile, delimiter=',')
        aircraft_writer.writerow([
            "Nation", "Flugzeug", "BattleRating", "Klasse",
            "Turnrate", "Steigrate", "Geschwindigkeit",
            "beiHoehe", "maxHoehe"
        ])
        for row in aircraft_list:
            values = [row.nation,
                      row.name,
                      row.battlerating,
                      row.plane_type,
                      row.turnrate,
                      row.climbrate,
                      row.speed,
                      row.speedheight,
                      row.maxheight]
            aircraft_writer.writerow(values)


def import_armaments(filename):  #BUG: Spuckt auch alles aus, was keinen Type hat
    armament_list = []
    with open(filename) as csvfile:
        armament_reader = csv.DictReader(csvfile, delimiter=',')
        for row in armament_reader:
            if row['Type'] in ('dumb bombs', 'retarded bombs',
                               'dumb rockets'):  #dann nur werte, die die Klasse Armament braucht
                armament = Class_Structure.Armament(
                    name=row['Name'],
                    armament_type=row['Type'],
                    projectile_mass=row['Projectile-Masse'],
                    explosive_type=row['Explosive-Type'],
                    explosive_mass=row['Explosive-Mass'],
                    TNT_equivalent=row['TNT-equivalent'],
                )
                armament_list.append(armament)

            if row['Type'] in ('guided bombs',):
                armament = Class_Structure.WeaponGuided(
                    name=row['Name'],
                    armament_type=row['Type'],
                    projectile_mass=row['Projectile-Masse'],
                    explosive_type=row['Explosive-Type'],
                    explosive_mass=row['Explosive-Mass'],
                    TNT_equivalent=row['TNT-equivalent'],
                    guidance=row['Guidance'],
                    missile_guidance_time=row['Missile-guidance-time']
                )
                armament_list.append(armament)

            if row['Type'] in ('Air-to-Ground',):
                armament = Class_Structure.AirToGroundRocketGuided(
                    name=row['Name'],
                    armament_type=row['Type'],
                    projectile_mass=row['Projectile-Masse'],
                    explosive_type=row['Explosive-Type'],
                    explosive_mass=row['Explosive-Mass'],
                    TNT_equivalent=row['TNT-equivalent'],
                    guidance=row['Guidance'],
                    missile_guidance_time=row['Missile-guidance-time'],
                    launch_range=row['Launch-range'],
                    maxspeed=row['Maximum-speed'],
                )
                armament_list.append(armament)

            if row['Type'] in ('Air-to-Air',):
                armament = Class_Structure.AirToAirRocket(
                    name=row['Name'],
                    armament_type=row['Type'],
                    projectile_mass=row['Projectile-Masse'],
                    explosive_type=row['Explosive-Type'],
                    explosive_mass=row['Explosive-Mass'],
                    TNT_equivalent=row['TNT-equivalent'],
                    guidance=row['Guidance'],
                    missile_guidance_time=row['Missile-guidance-time'],
                    launch_range=row['Launch-range'],
                    maxspeed=row['Maximum-speed'],
                    aspect=row['Aspect'],
                    lock_range=row['Lock-range-in-all-aspect'],
                    lock_range_rear=row['Lock-range-in-rear-aspect'],
                    maxg_overload=row['Maximum-Overload']
                )
                armament_list.append(armament)

            if row['Type'] in ('other'):
                armament = Class_Structure.Other_Armament(
                    name=row['Name'],
                    armament_type=row['Type'],
                    projectile_mass=row['Projectile-Masse'],
                )
                armament_list.append(armament)

    return armament_list


#Der hier ist mit Vorsicht zu geniessen, da ich nicht weiss wie das mit den ganzen leeren Feldern läuft.
#Stand 1.0 hatten wir das sowieso nicht auf dem Schirm, neue Waffen hinzufügen zu können.
def export_armaments(filename, armament_list):
    with open(filename, 'w', newline='') as csvfile:
        armament_writer = csv.writer(csvfile, delimiter=',')
        armament_writer.writerow([
            "Name", "Type", "Projectile-Masse", "Guidance",
            "Aspect", "Lock-range-in-rear-aspect", "Lock-range-in-all-aspect",
            "IRCCM", "Launch-range", "Maximum-speed", "Maximum-Overload",
            "Missile-guidance-time", "Explosive-Type", "Explosive-Mass",
            "TNT-equivalent"
        ]) #Header
        for row in armament_list:
            values = [getattr(row, "name", ""),
                      getattr(row, "armament_type", ""),
                      getattr(row, "projectile_mass", ""),
                      getattr(row, "guidance", ""),
                      getattr(row, "aspect", ""),
                      getattr(row, "lock_range_rear", ""),
                      getattr(row, "lock_range", ""),
                      getattr(row, "irccm", ""),
                      getattr(row, "launch_range", ""),
                      getattr(row, "maxspeed", ""),
                      getattr(row, "maxg_overload", ""),
                      getattr(row, "missile_guidance_time", ""),
                      getattr(row, "explosive_type", ""),
                      getattr(row, "explosive_mass", ""),
                      getattr(row, "TNT_equivalent", "")
            ]
            armament_writer.writerow(values)


def import_hardpoints(filename):
    hardpoint_list = []
    with open(filename) as csvfile:
        hardpoint_reader = csv.DictReader(csvfile, delimiter=',')
        #Da die CSV Dateien unterschiedliche Anzahlen an Pylonen haben, brauch ich erstmal die Anzahl:
        pylon_fields = hardpoint_reader.fieldnames[3:]
        #Und hier fasse ich die Pylonen in einer Liste zusammen
        for row in hardpoint_reader:
            pylon_list = []
            for pylon in pylon_fields:
                value = row.get(pylon)
                pylon_list.append(value)
            hardpoint = Class_Structure.Hardpoint(
                amount=row['Amount'],
                name=row['Pylon_Ges'],
                pylon_ges_anz=row['Pylon_Ges_Anz'],
                pylon_bool=pylon_list  #Beispiel: ['', 'True', 'True', 'True', 'True', 'True', '']
            )
            hardpoint_list.append(hardpoint)
        return hardpoint_list


#Kann nützlich sein, um die Nationen anzeigen zu lassen
'''
test = import_aircraft("Aircraft.csv")
testlist = set()
for i in test:
    testlist.add(i.nation)

print(testlist)
'''

#Gibt mir eine Waffenliste mit Typ
'''
test = import_armaments("Armament.csv")
testlist = set()
for i in test:
    testlist.add(i.name)
    print(f'{i.name}, {i.armament_type}')
'''

#Gibt mir alle Werte der Hardpoint Tabelle
'''
test = import_hardpoints('F-5C_Hardpoints.csv')
for i in test:
    print (f'{i.amount}, {i.name}, {i.pylon_ges_anz}, {i.pylon_bool}')
'''

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
