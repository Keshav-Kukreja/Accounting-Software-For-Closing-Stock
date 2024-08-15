import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('DATABASE.db')
conn.execute("DROP TABLE COMPANY_DATABASE")
conn.commit()
conn.close()