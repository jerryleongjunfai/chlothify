import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
import tabs as tabs
import functions #from functions.pyy


class ClothifyGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Clothify Store Management System")
        self.root.geometry("2000x14000")
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
            
            messagebox.showinfo("Database", "Connected to store.db successfully!")
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to connect to database: {str(e)}")
    
    def create_tables(self):
        """Create all necessary tables for the store"""
        
        # Only create tables that don't exist, checking existing schema first
        try:
            # Check if tables already exist to avoid duplicates
            self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            existing_tables = [row[0] for row in self.cursor.fetchall()]
            
            # Products table (only if not exists)
            if 'Product' not in existing_tables:
                self.cursor.execute("DROP TABLE IF EXISTS Product")
                self.cursor.execute('''
                    CREATE TABLE Product (
                        ProductID TEXT PRIMARY KEY,
                        ProductName TEXT NOT NULL,
                        ProductPrice REAL NOT NULL,
                        Category TEXT NOT NULL,
                        Size TEXT NOT NULL,
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
                        FOREIGN KEY (OrderID) REFERENCES Orders (OrderID),
                        FOREIGN KEY (ProductID) REFERENCES Products (ProductID)
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
                        FOREIGN KEY (OrderID) REFERENCES Orders (OrderID)
                    )
                ''')
            
            self.conn.commit()
        except Exception as e:
            print(f"Error creating tables: {e}")

    def create_widgets(self):
        """Create the main GUI widgets"""
        top_frame = tk.Frame(self.root, bg="#f0f0f0")
        top_frame.pack(fill='x')

        logout_btn = tk.Button(top_frame, text="Logout", command=self.logout, font=('Arial', 12),
                               bg="#e74c3c", fg="white")
        logout_btn.pack(side="right", padx=10, pady=10)

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


    def logout(self):
        functions.logout_user()
        self.root.destroy()
        show_login_window()  # ee-show login window after logout

    def __del__(self):
        """Close database connection when the object is destroyed"""
        if hasattr(self, 'conn'):
            self.conn.close()


#LOGIN WINDOW (before database GUI can be accessed window pops up)
def show_login_window():
    login_win = tk.Tk()
    login_win.title("Admin Login")
    login_win.geometry("2000x14000")
    login_win.configure(bg="#ffffff")

    # Centers username and password input
    container = tk.Frame(login_win, bg="#ffffff")
    container.pack(expand=True)

    tk.Label(container, text="Username:", font=('Arial', 14), bg="#ffffff").grid(row=0, column=0, padx=10, pady=10, sticky="e")
    username_entry = tk.Entry(container, font=('Arial', 14), width=25)
    username_entry.grid(row=0, column=1, padx=10, pady=10) #Username

    tk.Label(container, text="Password:", font=('Arial', 14), bg="#ffffff").grid(row=1, column=0, padx=10, pady=10, sticky="e")
    password_entry = tk.Entry(container, show="*", font=('Arial', 14), width=25)
    password_entry.grid(row=1, column=1, padx=10, pady=10) #Password

    def attempt_login():
        username = username_entry.get()
        password = password_entry.get()
        if functions.admin_login(username, password):
            login_win.destroy() 
            #LAUNCH DATABASE GUI!!!!!!!!!!!!!
            main_root = tk.Tk()
            app = ClothifyGUI(main_root)
            main_root.mainloop()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    login_btn = tk.Button(container, text="Login", command=attempt_login, font=('Arial', 14), bg="#3498db", fg="white")
    login_btn.grid(row=2, column=0, columnspan=2, pady=20)

    login_win.mainloop()

#Main Launch
if __name__ == "__main__":
    show_login_window() #shows the login window first, if password is right then it process database GUI
    
