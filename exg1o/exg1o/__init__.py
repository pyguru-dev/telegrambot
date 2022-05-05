import sqlite3

db = sqlite3.connect('DataBase.db')
sql = db.cursor()

sql.execute("""
	CREATE TABLE IF NOT EXISTS Accounts (
		Login TEXT,
		Email TEXT,
		Pasword BLOB
	)
""")