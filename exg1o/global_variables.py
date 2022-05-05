import threading
import sqlite3

lock = threading.Lock()
db = sqlite3.connect('DataBase.db', check_same_thread=False)
sql = db.cursor()