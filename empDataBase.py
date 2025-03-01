import sqlite3
import os

filepath = os.path.dirname(os.path.abspath(__file__))
conn = sqlite3.connect(filepath + "/" +"empDataBase.db")
conn.execute(
    """CREATE TABLE EMS
         (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
         NAME TEXT,
         POST TEXT,
         SALARY INTEGER);"""
)

conn.close()