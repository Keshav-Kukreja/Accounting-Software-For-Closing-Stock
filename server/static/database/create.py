import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('DATABASE.db')

# Create a cursor object using the cursor() method
cursor = conn.cursor()

cursor.execute("CREATE TABLE COMPANY_DATABASE (CODE INTEGER PRIMARY KEY, NAME TEXT NOT NULL);")

# Retrieve the list of all tables in the database
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

# Fetch all results
tables = cursor.fetchall()

#cursor.execute("INSERT INTO COMPANY_DATABASE (CODE,NAME) VALUES(1,'DEMO');")

cursor.execute("SELECT * FROM COMPANY_DATABASE;")

rows = cursor.fetchall()

for row in rows:
  print(row)

# Print the names of the tables
for table in tables:
    print(table[0])

# Close the connection
conn.close()
