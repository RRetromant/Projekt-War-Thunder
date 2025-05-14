import sqlite3
from Airplane import Airplane


class SqlWorker:
    def __init__(self, path: str):
        self.dbpath = path


    def addItem(self, plane: Airplane):
        query = f"INSERT INTO planes (nation, plane, battleRating, planeClass, turnrate, steigrate) VALUES (?,?,?,?,?,?)"
        tupel =(plane.nation, plane.plane,plane.battleRating, plane.planeClass, plane.turnrate, plane.steigrate)
        with sqlite3.connect(self.dbpath) as connection:
            cursor = connection.cursor()
            cursor.execute(query, tupel)
            connection.commit()

    #Liest alle EInträe aus der DB,
    def readItem(self):
        query = "SELECT * FROM planes"
        with sqlite3.connect(self.dbpath) as connection:
            cursor = connection.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            return rows

    #Muss einmal ausgeführt werden um die DB anzulegen
    def createTable(self):
        query = "CREATE TABLE IF NOT EXISTS planes ( nation TEXT, plane TEXT, battleRating FLOAT,planeClass Text, turnrate FLOAT, steigrate FLOAT)"
        with sqlite3.connect(self.dbpath) as connection:
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()



