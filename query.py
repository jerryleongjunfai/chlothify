import sqlite3

# Connect to existing database
conn = sqlite3.connect("store.db")
cursor = conn.cursor()

# Sample query: Get all products with stock < 10
cursor.execute("""
SELECT CustomerName, Email 
FROM Customer 
WHERE CustomerName = "Jerry";
""")

results = cursor.fetchall()

for row in results:
    print(row)

conn.close()