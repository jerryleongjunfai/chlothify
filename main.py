import sqlite3
import tkinter as tk

# Create the main window
root = tk.Tk()
root.title("Clothify GUI")
root.geometry("900x600")  # width x height

# Add a label
label = tk.Label(root, text="Welcome to Clothify!")
label.pack(pady=20)

# Add a button
def on_click():
    label.config(text="Button Clicked!")

button = tk.Button(root, text="Click Me", command=on_click)
button.pack()

# Start the GUI loop
root.mainloop()

# Connect to SQLite (creates a new file if not exists)
conn = sqlite3.connect("store.db")
cursor = conn.cursor()

# Create tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS Customer (
    CustomerID TEXT PRIMARY KEY,
    CustomerName TEXT NOT NULL,
    Email TEXT UNIQUE,
    Phone INTEGER NOT NULL,
    Address TEXT NOT NULL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Product (
    ProductID TEXT PRIMARY KEY,
    ProductName TEXT NOT NULL,
    ProductPrice DECIMAL(10, 2) NOT NULL,
    Category TEXT NOT NULL,
    Size TEXT NOT NULL,
    StockQty INTEGER NOT NULL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS OrderTable (
    OrderID TEXT PRIMARY KEY,
    OrderDate TEXT NOT NULL,
    TotalAmount DECIMAL(10, 2),
    CustomerID TEXT,
    FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID)
);
""")

print("edit made by liz")
print("liz made this edit")
cursor.execute("""
CREATE TABLE IF NOT EXISTS OrderItems (
    OrderItemID TEXT PRIMARY KEY,
    OrderID TEXT,
    ProductID TEXT,
    Quantity INTEGER,
    FOREIGN KEY (OrderID) REFERENCES OrderTable(OrderID),
    FOREIGN KEY (ProductID) REFERENCES Product(ProductID)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Payment (
    PaymentID TEXT PRIMARY KEY,
    OrderID TEXT,
    Amount DECIMAL(10, 2) NOT NULL,
    PaymentDate TEXT NOT NULL,
    PaymentMethod TEXT NOT NULL,
    FOREIGN KEY (OrderID) REFERENCES OrderTable(OrderID)
);
""")

conn.commit()
conn.close()
print("Database and tables created successfully.")
