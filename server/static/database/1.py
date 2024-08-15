import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('DATABASE.db')

# Create a cursor object using the cursor() method
cursor = conn.cursor()

# Retrieve the list of all tables in the database
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

# Fetch all results
tables = cursor.fetchall()

# Print the names of the tables
for table in tables:
    print(table[0])

for i in range(36):
  cursor.execute(f"INSERT INTO COMPANY_DATABASE (CODE,NAME) VALUES({i},'DEMO-{i}');")

conn.commit()

# Close the connection
conn.close()
