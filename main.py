import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
import tabs as tabs
import functions  # from functions.py
import auth as auth


class ClothifyGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Clothify Store Management System")
        self.root.geometry("1500x700")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize database connection
        self.init_database()
        
        # Create the main interface
        self.create_widgets()
        
    def init_database(self):
        """Initialize database connection and create tables if they don't exist"""
        try:
            self.conn = sqlite3.connect("store.db")
            self.cursor = self.conn.cursor()
            
            # Create tables if they don't exist
            self.create_tables()
            
            print("Connected to store.db successfully!")  # Changed from messagebox
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to connect to database: {str(e)}")
    
    def create_tables(self):
        """Create all necessary tables for the store"""
        
        # Only create tables that don't exist, checking existing schema first
        try:
            # Check if tables already exist to avoid duplicates
            self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            existing_tables = [row[0] for row in self.cursor.fetchall()]
            
            # Customer table (missing from original code)
            if 'Customer' not in existing_tables:
                self.cursor.execute('''
                    CREATE TABLE Customer (
                        CustomerID TEXT PRIMARY KEY,
                        CustomerName TEXT NOT NULL,
                        Email TEXT NOT NULL,
                        Phone TEXT NOT NULL CHECK(Phone GLOB '[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'),
                        Address TEXT NOT NULL
                    )
                ''')
            
            # Products table (only if not exists)
            if 'Product' not in existing_tables:
                self.cursor.execute("DROP TABLE IF EXISTS Product")
                self.cursor.execute('''
                    CREATE TABLE Product (
                        ProductID TEXT PRIMARY KEY,
                        ProductName TEXT NOT NULL,
                        ProductPrice REAL NOT NULL,
                        Category TEXT NOT NULL,
                        Size TEXT NOT NULL CHECK(Size GLOB '[A-Za-z]*'),
                        StockQty INTEGER NOT NULL  
                    )
                ''')
            
            # Orders table (only if not exists)  
            if 'OrderTable' not in existing_tables:
                self.cursor.execute('''
                    CREATE TABLE OrderTable (
                        OrderID TEXT PRIMARY KEY,
                        CustomerID TEXT NOT NULL,
                        OrderDate TEXT NOT NULL,
                        TotalAmount REAL NOT NULL,
                        Status TEXT NOT NULL DEFAULT 'Pending',
                        FOREIGN KEY (CustomerID) REFERENCES Customer (CustomerID)
                    )
                ''')
            
            # OrderItems table (only if not exists)
            if 'OrderItems' not in existing_tables:
                self.cursor.execute('''
                    CREATE TABLE OrderItems (
                        OrderItemID INTEGER PRIMARY KEY AUTOINCREMENT,
                        OrderID TEXT NOT NULL,
                        ProductID TEXT NOT NULL,
                        Quantity INTEGER NOT NULL,
                        UnitPrice REAL NOT NULL,
                        FOREIGN KEY (OrderID) REFERENCES OrderTable (OrderID),
                        FOREIGN KEY (ProductID) REFERENCES Product (ProductID)
                    )
                ''')
            
            # Payments table (only if not exists)
            if 'Payment' not in existing_tables:
                self.cursor.execute('''
                    CREATE TABLE Payment (
                        PaymentID TEXT PRIMARY KEY,
                        OrderID TEXT NOT NULL,
                        PaymentDate TEXT NOT NULL,
                        Amount REAL NOT NULL,
                        PaymentMethod TEXT NOT NULL,
                        Status TEXT NOT NULL DEFAULT 'Pending',
                        FOREIGN KEY (OrderID) REFERENCES OrderTable (OrderID)
                    )
                ''')
            
            self.conn.commit()
        except Exception as e:
            print(f"Error creating tables: {e}")

    def create_widgets(self):
        """Create the main GUI widgets"""
        top_frame = tk.Frame(self.root, bg="#f0f0f0")
        top_frame.pack(fill='x')

        logout_btn_gradient = tk.Button(
            top_frame, text="Logout", 
            command=self.logout, 
            font=('Arial', 12, 'bold'), 
            bg="#c0392b",  # Darker red
            fg="black",
            activebackground="#a93226",  # Darker when clicked
            activeforeground="white",
            relief="flat",
            bd=0,
            padx=25,
            pady=10,
            cursor="hand2"
        )
        logout_btn_gradient.pack(side="right", padx=10, pady=10)

        # Title
        title_label = tk.Label(self.root, text="Clothify Store Management System", 
                              font=('Arial', 16, 'bold'), bg='#f0f0f0', fg='#333')
        title_label.pack(pady=10)

        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create tabs
        tabs.create_customer_tab(self)
        tabs.create_product_tab(self)
        tabs.create_order_tab(self)
        tabs.create_payment_tab(self)
        tabs.create_sql_tab(self)

    def logout(self):
        functions.logout_user()
        self.root.destroy()
        auth.show_login_window()  # re-show login window after logout

    def __del__(self):
        """Close database connection when the object is destroyed"""
        if hasattr(self, 'conn'):
            self.conn.close()

# Main Launch
if __name__ == "__main__":
    auth.show_login_window()  # shows the login window first, if password is right then it processes database GUI