import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
import tabs as tabs
import functions  # from functions.py


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
                        Phone TEXT NOT NULL,
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
        show_login_window()  # re-show login window after logout

    def __del__(self):
        """Close database connection when the object is destroyed"""
        if hasattr(self, 'conn'):
            self.conn.close()


# LOGIN WINDOW (before database GUI can be accessed window pops up)
def show_login_window():
    login_win = tk.Tk()
    login_win.title("Clothify Admin Login")
    login_win.geometry("450x700")  # Increased height to ensure button is visible
    login_win.configure(bg="#f5f5f5")
    login_win.resizable(False, False)
    
    # Center the window on screen
    login_win.update_idletasks()
    x = (login_win.winfo_screenwidth() // 2) - (450 // 2)
    y = (login_win.winfo_screenheight() // 2) - (700 // 2)  # Updated for new height
    login_win.geometry(f"450x700+{x}+{y}")

    # Main container with gradient-like effect
    main_container = tk.Frame(login_win, bg="#f5f5f5")
    main_container.pack(fill='both', expand=True, padx=30, pady=30)

    # Header section
    header_frame = tk.Frame(main_container, bg="#f5f5f5")
    header_frame.pack(pady=(20, 40))

    # App logo/icon (using text for now)
    logo_frame = tk.Frame(header_frame, bg="#2196F3", width=80, height=80)
    logo_frame.pack_propagate(False)
    logo_frame.pack(pady=(0, 20))
    
    logo_label = tk.Label(logo_frame, text="C", font=('Arial', 32, 'bold'), 
                         bg="#2196F3", fg="white")
    logo_label.place(relx=0.5, rely=0.5, anchor='center')

    # Title
    title_label = tk.Label(header_frame, text="Clothify Admin", 
                          font=('Segoe UI', 24, 'bold'), 
                          bg="#f5f5f5", fg="#333333")
    title_label.pack()

    subtitle_label = tk.Label(header_frame, text="Store Management System", 
                             font=('Segoe UI', 12), 
                             bg="#f5f5f5", fg="#666666")
    subtitle_label.pack(pady=(5, 0))

    # Login form container
    form_container = tk.Frame(main_container, bg="white", relief='flat')
    form_container.pack(pady=20, padx=20, fill='x')
    
    # Add some padding inside the form
    form_inner = tk.Frame(form_container, bg="white")
    form_inner.pack(padx=40, pady=40, fill='x')

    # Username field with placeholder
    username_label = tk.Label(form_inner, text="Username", 
                             font=('Segoe UI', 11, 'bold'), 
                             bg="white", fg="#555555")
    username_label.pack(anchor='w', pady=(0, 5))
    
    username_frame = tk.Frame(form_inner, bg="white", highlightbackground="#e0e0e0", 
                             highlightthickness=1, relief='flat')
    username_frame.pack(fill='x', pady=(0, 20))
    
    username_entry = tk.Entry(username_frame, font=('Segoe UI', 12), 
                             bg="white", fg="#999999", relief='flat', bd=0)
    username_entry.pack(padx=15, pady=12, fill='x')
    
    # Set placeholder text
    username_placeholder = "Enter your username"
    username_entry.insert(0, username_placeholder)

    # Password field with placeholder
    password_label = tk.Label(form_inner, text="Password", 
                             font=('Segoe UI', 11, 'bold'), 
                             bg="white", fg="#555555")
    password_label.pack(anchor='w', pady=(0, 5))
    
    password_frame = tk.Frame(form_inner, bg="white", highlightbackground="#e0e0e0", 
                             highlightthickness=1, relief='flat')
    password_frame.pack(fill='x', pady=(0, 30))
    
    password_entry = tk.Entry(password_frame, font=('Segoe UI', 12), 
                             bg="white", fg="#999999", relief='flat', bd=0)
    password_entry.pack(padx=15, pady=12, fill='x')
    
    # Set placeholder text
    password_placeholder = "Enter your password"
    password_entry.insert(0, password_placeholder)
    password_is_placeholder = True

    # Placeholder and focus effects for username
    def on_username_focus_in(event):
        username_frame.configure(highlightbackground="#2196F3", highlightthickness=2)
        if username_entry.get() == username_placeholder:
            username_entry.delete(0, 'end')
            username_entry.configure(fg="#333333")
    
    def on_username_focus_out(event):
        username_frame.configure(highlightbackground="#e0e0e0", highlightthickness=1)
        if not username_entry.get():
            username_entry.insert(0, username_placeholder)
            username_entry.configure(fg="#999999")

    # Placeholder and focus effects for password
    def on_password_focus_in(event):
        nonlocal password_is_placeholder
        password_frame.configure(highlightbackground="#2196F3", highlightthickness=2)
        if password_is_placeholder:
            password_entry.delete(0, 'end')
            password_entry.configure(show="*", fg="#333333")
            password_is_placeholder = False
    
    def on_password_focus_out(event):
        nonlocal password_is_placeholder
        password_frame.configure(highlightbackground="#e0e0e0", highlightthickness=1)
        if not password_entry.get():
            password_entry.configure(show="", fg="#999999")
            password_entry.insert(0, password_placeholder)
            password_is_placeholder = True
    
    username_entry.bind("<FocusIn>", on_username_focus_in)
    username_entry.bind("<FocusOut>", on_username_focus_out)
    password_entry.bind("<FocusIn>", on_password_focus_in)
    password_entry.bind("<FocusOut>", on_password_focus_out)

    def attempt_login():
        username = username_entry.get()
        password = password_entry.get()
        
        # Check if placeholder text is still present
        if username == username_placeholder or not username:
            messagebox.showerror("Login Failed", "Please enter your username")
            return
        
        if password == password_placeholder or not password:
            messagebox.showerror("Login Failed", "Please enter your password")
            return
            
        if functions.admin_login(username, password):
            login_win.destroy() 
            # LAUNCH DATABASE GUI
            main_root = tk.Tk()
            app = ClothifyGUI(main_root)
            main_root.mainloop()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    # Login button - Simple and clear approach
    login_btn = tk.Button(form_inner, text="LOGIN", command=attempt_login, 
                         font=('Segoe UI', 14, 'bold'), 
                         bg="#2196F3", fg="black", 
                         relief='flat', bd=0, 
                         activebackground="#1976D2", activeforeground="black",
                         cursor="hand2", 
                         width=25, height=2)
    login_btn.pack(pady=(30, 20))

    # Hover effects for the button
    def on_button_enter(e):
        login_btn.configure(bg="#1976D2")
    
    def on_button_leave(e):
        login_btn.configure(bg="#2196F3")
    
    login_btn.bind("<Enter>", on_button_enter)
    login_btn.bind("<Leave>", on_button_leave)

    # Enter key binding
    def on_enter_key(event):
        attempt_login()
    
    login_win.bind('<Return>', on_enter_key)
    username_entry.bind('<Return>', on_enter_key)
    password_entry.bind('<Return>', on_enter_key)

    # Footer
    footer_frame = tk.Frame(main_container, bg="#f5f5f5")
    footer_frame.pack(side='bottom', pady=(40, 0))
    
    footer_label = tk.Label(footer_frame, text="© 2025 Clothify Store Management", 
                           font=('Segoe UI', 9), 
                           bg="#f5f5f5", fg="#999999")
    footer_label.pack()

    # Set focus to username field
    username_entry.focus_set()

    login_win.mainloop()


# Main Launch
if __name__ == "__main__":
    show_login_window()  # shows the login window first, if password is right then it processes database GUI