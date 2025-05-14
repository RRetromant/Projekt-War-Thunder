import sqlite3
from Airplane import Airplane
from SQLWorker import SqlWorker

plane = Airplane("Deutschland", "Bf109-F4", 4.0, "Jaeger", 19, 20)

path_dir: str = r"C:\Users\Kuehn\Desktop\Dev\test.db"
sql = SqlWorker(path_dir)

sql.addItem(plane)

planes = sql.readItem()

print(planes)
