import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
import tabs as tabs

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

        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create tabs
        tabs.create_customer_tab(self)
        tabs.create_product_tab(self)
        tabs.create_order_tab(self)
        tabs.create_payment_tab(self)

def __del__(self):
        """Close database connection when the object is destroyed"""
        if hasattr(self, 'conn'):
            self.conn.close()


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
