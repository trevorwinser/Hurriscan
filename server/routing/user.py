import os
import sqlite3


currentUsername = "";

basedir = os.path.abspath(os.path.dirname(__file__))
DB_NAME = 'hurriscan.db'
 
conn = sqlite3.connect(os.path.join(basedir, DB_NAME))
conn.row_factory = sqlite3.Row
cursor = conn.cursor()
    
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
rows = cursor.fetchall()
print(rows)
for row in rows:
    print(row)