import sqlite3

conn = sqlite3.connect("store.db")
cursor = conn.cursor()

cursor.execute("""
INSERT INTO Customer (CustomerID, CustomerName, Email, Phone, Address)
VALUES ('C001', 'Jerry Leong', 'jerry@example.com', 1234567890, 'Kuala Lumpur');
""")

cursor.execute("""
INSERT INTO Product (ProductID, ProductName, ProductPrice, Category, Size, StockQty)
VALUES ('P001', 'Black T-Shirt', 49.90, 'T-Shirts', 'M', 5);
""")

conn.commit()
conn.close()