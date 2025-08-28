from datetime import datetime
from tkinter import messagebox, simpledialog, ttk
import sqlite3
import tkinter as tk

# Helper functions
def clear_product_entries(app):
    """Clear all product entry fields"""
    for entry in app.product_entries.values():
        entry.delete(0, 'end')

#------------------------------AUTHENTICATION---------------------------------------------
USER_SESSIONS = {"current_user": None}

def validate_credentials(username, password):
    # username: password
    valid_admins = {
        "admin": "clothify123",
        "employee": "clothify123"
    }
    return valid_admins.get(username) == password

def admin_login(username, password):
    """Login function that also sets session (optional)"""
    if validate_credentials(username, password):
        USER_SESSIONS["current_user"] = username
        return True
    return False

def logout_user():
    """Clears the current session"""
    USER_SESSIONS["current_user"] = None

#-------------------------------Customer Management--------------------------------------------------
def add_customer(app):
        """Add a new customer"""
        def save_customer():
            try:
                customer_id = id_entry.get()
                name = name_entry.get()
                email = email_entry.get()
                phone = phone_entry.get()
                address = address_entry.get()
                
                if not all([customer_id, name, email, phone, address]):
                    messagebox.showerror("Error", "All fields are required!")
                    return
            
                # Phone validation: must be exactly 9 digits
                if not phone.isdigit() or len(phone) != 9:
                    messagebox.showerror("Error", "Phone number must contain exactly 9 digits!")
                    return
            
                app.cursor.execute("""
                    INSERT INTO Customer (CustomerID, CustomerName, Email, Phone, Address)
                    VALUES (?, ?, ?, ?, ?)
                """, (customer_id, name, email, phone, address))

                app.conn.commit()
                messagebox.showinfo("Success", "Customer added successfully!")
                add_window.destroy()
                view_customers(app)  # Refresh the view

            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Customer ID already exists!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add customer: {str(e)}")
        
        # Create add customer window
        add_window = tk.Toplevel(app.root)
        add_window.title("Add New Customer")
        add_window.geometry("400x500")
        
        # Form fields
        tk.Label(add_window, text="Customer ID:").pack(pady=5)
        id_entry = tk.Entry(add_window, width=30)
        id_entry.pack(pady=5)
        
        tk.Label(add_window, text="Name:").pack(pady=5)
        name_entry = tk.Entry(add_window, width=30)
        name_entry.pack(pady=5)
        
        tk.Label(add_window, text="Email:").pack(pady=5)
        email_entry = tk.Entry(add_window, width=30)
        email_entry.pack(pady=5)
        
        tk.Label(add_window, text="Phone:").pack(pady=5)
        phone_entry = tk.Entry(add_window, width=30)
        phone_entry.pack(pady=5)
        
        tk.Label(add_window, text="Address:").pack(pady=5)
        address_entry = tk.Entry(add_window, width=30)
        address_entry.pack(pady=5)
        
        tk.Button(add_window, text="Save Customer", command=save_customer,
                 bg='#4CAF50', fg='black', font=('Arial', 15, 'bold')).pack(pady=20)

def view_customers(app):
        """Display all customers in the treeview"""
        for item in app.customer_tree.get_children():
            app.customer_tree.delete(item)

        try:
            app.cursor.execute("SELECT * FROM Customer")
            customers = app.cursor.fetchall()
            
            for customer in customers:
                app.customer_tree.insert('', 'end', values=customer)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch customers: {str(e)}")

def search_customer(app):
        """Search for customers by name or email"""
        search_term = simpledialog.askstring("Search Customer", "Enter customer name or email:")
        if not search_term:
            return

        for item in app.customer_tree.get_children():
            app.customer_tree.delete(item)
        
        try:
            app.cursor.execute("""
                SELECT * FROM Customer 
                WHERE CustomerName LIKE ? OR Email LIKE ?
            """, (f'%{search_term}%', f'%{search_term}%'))

            customers = app.cursor.fetchall()
            
            for customer in customers:
                app.customer_tree.insert('', 'end', values=customer)

            if not customers:
                messagebox.showinfo("Search Results", "No customers found matching your search.")
        except Exception as e:
            messagebox.showerror("Error", f"Search failed: {str(e)}")            

def update_customer(app):
    """GUI function to update customer data"""
    # Get selected item from treeview
    selected_item = app.customer_tree.selection()
    
    if not selected_item:
        messagebox.showwarning("Warning", "Please select a customer to update.")
        return
    
    # Get customer data from selected row
    customer_data = app.customer_tree.item(selected_item[0])['values']
    customer_id = customer_data[0]
    current_name = customer_data[1]
    current_email = customer_data[2]
    current_phone = customer_data[3]
    current_address = customer_data[4]
    
    # Create update window
    update_window = tk.Toplevel(app.root)
    update_window.title("Update Customer")
    update_window.geometry("400x500")
    update_window.resizable(False, False)
    
    # Center the window
    update_window.transient(app.root)
    update_window.grab_set()
    
    # Create form fields
    tk.Label(update_window, text="Update Customer Information", 
             font=('Arial', 14, 'bold')).pack(pady=10)
    
    # Name field
    tk.Label(update_window, text="Name:").pack(anchor='w', padx=20)
    name_var = tk.StringVar(value=current_name)
    name_entry = tk.Entry(update_window, textvariable=name_var, width=40)
    name_entry.pack(pady=5, padx=20)
    
    # Email field
    tk.Label(update_window, text="Email:").pack(anchor='w', padx=20)
    email_var = tk.StringVar(value=current_email)
    email_entry = tk.Entry(update_window, textvariable=email_var, width=40)
    email_entry.pack(pady=5, padx=20)
    
    # Phone field
    tk.Label(update_window, text="Phone:").pack(anchor='w', padx=20)
    phone_var = tk.StringVar(value=current_phone)
    phone_entry = tk.Entry(update_window, textvariable=phone_var, width=40)
    phone_entry.pack(pady=5, padx=20)
    
    # Address field
    tk.Label(update_window, text="Address:").pack(anchor='w', padx=20)
    address_var = tk.StringVar(value=current_address)
    address_entry = tk.Entry(update_window, textvariable=address_var, width=40)
    address_entry.pack(pady=5, padx=20)
    
    def save_updates():
        """Save the updated customer information"""
        new_name = name_var.get().strip()
        new_email = email_var.get().strip()
        new_phone = phone_var.get().strip()
        new_address = address_var.get().strip()
        
        # Validate required fields
        if not new_name or not new_email:
            messagebox.showerror("Error", "Name and Email are required fields.")
            return
        if not new_phone.isdigit() or len(new_phone) != 9:
            messagebox.showerror("Error", "Phone number must contain exactly 9 digits!")
            return
        
        try:
            # Update customer in database (assuming you have a database connection object)
            cursor = app.cursor  
            
            # Update all fields at once
            cursor.execute("""
                UPDATE Customer 
                SET CustomerName = ?, Email = ?, Phone = ?, Address = ? 
                WHERE CustomerID = ?
            """, (new_name, new_email, new_phone, new_address, customer_id))
            
            app.conn.commit()  
            
            # Update the treeview
            app.customer_tree.item(selected_item[0], values=(
                customer_id, new_name, new_email, new_phone, new_address
            ))
            
            messagebox.showinfo("Success", "Customer updated successfully!")
            update_window.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update customer: {e}")
    
    # Buttons
    btn_frame = tk.Frame(update_window)
    btn_frame.pack(pady=20)
    
    tk.Button(btn_frame, text="Save Changes", command=save_updates,
              bg='#4CAF50', fg='black', font=('Arial', 15, 'bold')).pack(side='left', padx=5)
    tk.Button(btn_frame, text="Cancel", command=update_window.destroy,
              bg='#f44336', fg='black', font=('Arial', 15, 'bold')).pack(side='left', padx=5)

def delete_customer(app):
    """GUI function to delete customer data"""
    # Get selected item from treeview
    selected_item = app.customer_tree.selection()
    
    if not selected_item:
        messagebox.showwarning("Warning", "Please select a customer to delete.")
        return
    
    # Get customer data from selected row
    customer_data = app.customer_tree.item(selected_item[0])['values']
    customer_id = customer_data[0]
    customer_name = customer_data[1]
    
    # Confirm deletion
    confirm = messagebox.askyesno(
        "Confirm Deletion", 
        f"Are you sure you want to delete customer '{customer_name}' (ID: {customer_id})?\n\n"
        "This action cannot be undone."
    )
    
    if not confirm:
        return
    
    try:
        # Delete customer from database
        cursor = app.cursor  # Adjust this to your database connection
        cursor.execute("DELETE FROM Customer WHERE CustomerID = ?", (customer_id,))
        app.conn.commit()  # Adjust this to your database connection
        
        # Remove from treeview
        app.customer_tree.delete(selected_item[0])
        
        messagebox.showinfo("Success", "Customer deleted successfully!")
        
    except Exception as e:
        messagebox.showerror("Error", f"Failed to delete customer: {e}")

#-------------------------------------------PRODUCT MANAGEMENT---------------------------------
def add_product(app):
    """Add a new product"""
    def save_product():
        try:
            product_id = id_entry.get()
            name = name_entry.get()
            price = price_entry.get()
            category = category_entry.get()
            size = size_entry.get()
            stock = stock_entry.get()
            
            if not all([product_id, name, price, category, size, stock]):
                messagebox.showerror("Error", "All fields are required!")
                return
            
            if not new_size.isalpha():
                messagebox.showerror("Error", "Size must only contain letters (e.g., S, M, L, XL).")
                return

            try:
                price = float(price)
                stock = int(stock)
            except ValueError:
                messagebox.showerror("Error", "Price must be a number and StockQty must be an integer!")
                return
            
            app.cursor.execute("""
                INSERT INTO Product (ProductID, ProductName, ProductPrice, Category, Size, StockQty)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (product_id, name, price, category, size, stock))

            app.conn.commit()
            messagebox.showinfo("Success", "Product added successfully!")
            add_window.destroy()
            view_products(app)  # Refresh the view

        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Product ID already exists!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add product: {str(e)}")
    
    # Create add product window
    add_window = tk.Toplevel(app.root)
    add_window.title("Add New Product")
    add_window.geometry("400x500")
    
    # Form fields
    tk.Label(add_window, text="Product ID:").pack(pady=5)
    id_entry = tk.Entry(add_window, width=30)
    id_entry.pack(pady=5)
    
    tk.Label(add_window, text="Name:").pack(pady=5)
    name_entry = tk.Entry(add_window, width=30)
    name_entry.pack(pady=5)
    
    tk.Label(add_window, text="Price:").pack(pady=5)
    price_entry = tk.Entry(add_window, width=30)
    price_entry.pack(pady=5)

    tk.Label(add_window, text="Category:").pack(pady=5)
    category_entry = tk.Entry(add_window, width=30)
    category_entry.pack(pady=5)
    

    tk.Label(add_window, text="Size").pack(pady=5)   
    size_entry = tk.Entry(add_window, width=30)                
    size_entry.pack(pady=5)                
    
    tk.Label(add_window, text="StockQty:").pack(pady=5)
    stock_entry = tk.Entry(add_window, width=30)
    stock_entry.pack(pady=5)
    
    tk.Button(add_window, text="Save Product", command=save_product,
             bg='#4CAF50', fg='black', font=('Arial', 15, 'bold')).pack(pady=20)


def view_products(app):
    """Display all products in the treeview"""
    for item in app.product_tree.get_children():
        app.product_tree.delete(item)

    try:
        app.cursor.execute("SELECT * FROM Product")
        products = app.cursor.fetchall()
        
        for product in products:
            app.product_tree.insert('', 'end', values=product)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch products: {str(e)}")


def search_product(app):
    """Search for products by name or category"""
    search_term = simpledialog.askstring("Search Product", "Enter product name or category:")
    if not search_term:
        return

    for item in app.product_tree.get_children():
        app.product_tree.delete(item)
    
    try:
        app.cursor.execute("""
            SELECT * FROM Product 
            WHERE ProductName LIKE ? OR Category LIKE ?
        """, (f'%{search_term}%', f'%{search_term}%'))

        products = app.cursor.fetchall()
        
        for product in products:
            app.product_tree.insert('', 'end', values=product)

        if not products:
            messagebox.showinfo("Search Results", "No products found matching your search.")
    except Exception as e:
        messagebox.showerror("Error", f"Search failed: {str(e)}")


def update_product(app):
    """GUI function to update product data"""
    # Get selected item from treeview
    selected_item = app.product_tree.selection()
    
    if not selected_item:
        messagebox.showwarning("Warning", "Please select a product to update.")
        return
    
    # Get product data from selected row
    product_data = app.product_tree.item(selected_item[0])['values']
    product_id = product_data[0]
    current_name = product_data[1]
    current_price = product_data[2]
    current_category = product_data[3]
    current_size = product_data[4]
    current_stock = product_data[5]
    
    # Create update window
    update_window = tk.Toplevel(app.root)
    update_window.title("Update Product")
    update_window.geometry("400x500")
    update_window.resizable(False, False)
    
    # Center the window
    update_window.transient(app.root)
    update_window.grab_set()
    
    # Create form fields
    tk.Label(update_window, text="Update Product Information", 
             font=('Arial', 14, 'bold')).pack(pady=10)
    
    # Name field
    tk.Label(update_window, text="Name:").pack(anchor='w', padx=20)
    name_var = tk.StringVar(value=current_name)
    name_entry = tk.Entry(update_window, textvariable=name_var, width=40)
    name_entry.pack(pady=5, padx=20)
    
    # Price field
    tk.Label(update_window, text="Price:").pack(anchor='w', padx=20)
    price_var = tk.StringVar(value=current_price)
    price_entry = tk.Entry(update_window, textvariable=price_var, width=40)
    price_entry.pack(pady=5, padx=20)

    # Category field
    tk.Label(update_window, text="Category:").pack(anchor='w', padx=20)
    category_var = tk.StringVar(value=current_category)
    category_entry = tk.Entry(update_window, textvariable=category_var, width=40)
    category_entry.pack(pady=5, padx=20)
    
    # Size field
    tk.Label(update_window, text="Size:").pack(anchor='w', padx=20)
    size_var = tk.StringVar(value=current_size)
    size_entry = tk.Entry(update_window, textvariable=size_var, width=40)
    size_entry.pack(pady=5, padx=20)

    # Stock field
    tk.Label(update_window, text="StockQty:").pack(anchor='w', padx=20)
    stock_var = tk.StringVar(value=current_stock)
    stock_entry = tk.Entry(update_window, textvariable=stock_var, width=40)
    stock_entry.pack(pady=5, padx=20)
    
    def save_updates():
        """Save the updated product information"""
        new_name = name_var.get().strip()
        new_price = price_var.get().strip()
        new_category = category_var.get().strip()
        new_size = size_var.get().strip()
        new_stock = stock_var.get().strip()
        
        if not new_name or not new_category or not new_price or not new_stock:
            messagebox.showerror("Error", "All fields are required.")
            return
        
        if not new_size.isalpha():
            messagebox.showerror("Error", "Size must only contain letters (e.g., S, M, L, XL).")
            return
        
        try:
            new_price = float(new_price)
            new_stock = int(new_stock)
        except ValueError:
            messagebox.showerror("Error", "Price must be a number and Stock must be an integer!")
            return

        try:
            cursor = app.cursor  
            
            cursor.execute("""
                UPDATE Product 
                SET ProductName = ?, ProductPrice = ?, Category = ?, Size = ?, StockQty = ? 
                WHERE ProductID = ?
            """, (new_name, new_price, new_category, new_size, new_stock, product_id))
            
            app.conn.commit()  
            
            app.product_tree.item(selected_item[0], values=(
                product_id, new_name, new_price, new_category, new_size, new_stock
            ))
            
            messagebox.showinfo("Success", "Product updated successfully!")
            update_window.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update product: {e}")
    
    # Buttons
    btn_frame = tk.Frame(update_window)
    btn_frame.pack(pady=20)
    
    tk.Button(btn_frame, text="Save Changes", command=save_updates,
              bg='#4CAF50', fg='black', font=('Arial', 15, 'bold')).pack(side='left', padx=5)
    tk.Button(btn_frame, text="Cancel", command=update_window.destroy,
              bg='#f44336', fg='black', font=('Arial', 15, 'bold')).pack(side='left', padx=5)


def delete_product(app):
    """GUI function to delete product data"""
    selected_item = app.product_tree.selection()
    
    if not selected_item:
        messagebox.showwarning("Warning", "Please select a product to delete.")
        return
    
    product_data = app.product_tree.item(selected_item[0])['values']
    product_id = product_data[0]
    product_name = product_data[1]
    
    confirm = messagebox.askyesno(
        "Confirm Deletion", 
        f"Are you sure you want to delete product '{product_name}' (ID: {product_id})?\n\n"
        "This action cannot be undone."
    )
    
    if not confirm:
        return
    
    try:
        cursor = app.cursor
        cursor.execute("DELETE FROM Product WHERE ProductID = ?", (product_id,))
        app.conn.commit()
        
        app.product_tree.delete(selected_item[0])
        
        messagebox.showinfo("Success", "Product deleted successfully!")
        
    except Exception as e:
        messagebox.showerror("Error", f"Failed to delete product: {e}")

#-------------------------------Order Management--------------------------------------------------------

def view_orders(app):
        """Display all orders"""
        for item in app.order_tree.get_children():
            app.order_tree.delete(item)
        
        try:
            app.cursor.execute("SELECT * FROM OrderTable")
            orders = app.cursor.fetchall()
            
            for order in orders:
                app.order_tree.insert('', 'end', values=order)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch orders: {str(e)}")
def create_order(app):
    """Add a new order with complete form and automatic payment creation"""
    
    # Create order window
    add_window = tk.Toplevel(app.root)
    add_window.title("Add New Order")
    add_window.geometry("450x700")
    add_window.resizable(False, False)
    add_window.transient(app.root)
    add_window.grab_set()
    
    # Configure window background
    add_window.configure(bg='#f0f0f0')
    
    # Title
    title_label = tk.Label(add_window, text="Add New Order", 
                          font=('Arial', 18, 'bold'), bg='#f0f0f0', fg='#333')
    title_label.pack(pady=15)
    
    # Main form frame with better styling
    form_frame = tk.Frame(add_window, bg='#f0f0f0')
    form_frame.pack(pady=10, padx=30, fill='both', expand=True)
    
    # Order ID
    tk.Label(form_frame, text="Order ID:", font=('Arial', 12, 'bold'), 
             bg='#f0f0f0', fg='#333').grid(row=0, column=0, sticky='w', pady=10)
    order_id_entry = tk.Entry(form_frame, width=25, font=('Arial', 11))
    order_id_entry.grid(row=0, column=1, pady=10, padx=(10, 0), sticky='w')
    
    # Customer ID
    tk.Label(form_frame, text="Customer ID:", font=('Arial', 12, 'bold'), 
             bg='#f0f0f0', fg='#333').grid(row=1, column=0, sticky='w', pady=10)
    customer_id_entry = tk.Entry(form_frame, width=25, font=('Arial', 11))
    customer_id_entry.grid(row=1, column=1, pady=10, padx=(10, 0), sticky='w')
    
    # Order Date
    tk.Label(form_frame, text="Date:", font=('Arial', 12, 'bold'), 
             bg='#f0f0f0', fg='#333').grid(row=2, column=0, sticky='w', pady=10)
    order_date_entry = tk.Entry(form_frame, width=25, font=('Arial', 11))
    order_date_entry.grid(row=2, column=1, pady=10, padx=(10, 0), sticky='w')
    # Pre-fill with current date
    order_date_entry.insert(0, datetime.now().strftime("%d/%m/%Y"))

    # Total Amount
    tk.Label(form_frame, text="Amount:", font=('Arial', 12, 'bold'), 
             bg='#f0f0f0', fg='#333').grid(row=3, column=0, sticky='w', pady=10)
    total_amount_entry = tk.Entry(form_frame, width=25, font=('Arial', 11))
    total_amount_entry.grid(row=3, column=1, pady=10, padx=(10, 0), sticky='w')
    
    # Order Status Dropdown
    tk.Label(form_frame, text="Order Status:", font=('Arial', 12, 'bold'), 
             bg='#f0f0f0', fg='#333').grid(row=4, column=0, sticky='w', pady=10)
    status_var = tk.StringVar(value="Pending")
    status_dropdown = ttk.Combobox(form_frame, textvariable=status_var, 
                                  width=22, font=('Arial', 11))
    status_dropdown['values'] = ("Pending", "Processing", "Completed", "Cancelled")
    status_dropdown['state'] = 'readonly'  # Make it read-only
    status_dropdown.grid(row=4, column=1, pady=10, padx=(10, 0), sticky='w')
    
    # Separator line
    separator = ttk.Separator(form_frame, orient='horizontal')
    separator.grid(row=5, column=0, columnspan=2, sticky='ew', pady=20)
    
    # Payment section title
    payment_title = tk.Label(form_frame, text="Payment Information", 
                            font=('Arial', 14, 'bold'), bg='#f0f0f0', fg='#2196F3')
    payment_title.grid(row=6, column=0, columnspan=2, pady=(10, 15))
    
    # Payment Method Dropdown
    tk.Label(form_frame, text="Payment Method:", font=('Arial', 12, 'bold'), 
             bg='#f0f0f0', fg='#333').grid(row=7, column=0, sticky='w', pady=10)
    payment_method_var = tk.StringVar(value="Cash")
    payment_method_dropdown = ttk.Combobox(form_frame, textvariable=payment_method_var, 
                                          width=22, font=('Arial', 11))
    payment_method_dropdown['values'] = ("Cash", "Credit Card", "Debit Card", 
                                        "Bank Transfer", "Digital Wallet", "Check")
    payment_method_dropdown['state'] = 'readonly'
    payment_method_dropdown.grid(row=7, column=1, pady=10, padx=(10, 0), sticky='w')
    
    # Payment Date
    tk.Label(form_frame, text="Payment Date:", font=('Arial', 12, 'bold'), 
             bg='#f0f0f0', fg='#333').grid(row=8, column=0, sticky='w', pady=10)
    payment_date_entry = tk.Entry(form_frame, width=25, font=('Arial', 11))
    payment_date_entry.grid(row=8, column=1, pady=10, padx=(10, 0), sticky='w')
    # Pre-fill with current date
    payment_date_entry.insert(0, datetime.now().strftime("%d/%m/%Y"))

    # Payment Status Dropdown
    tk.Label(form_frame, text="Payment Status:", font=('Arial', 12, 'bold'), 
             bg='#f0f0f0', fg='#333').grid(row=9, column=0, sticky='w', pady=10)
    payment_status_var = tk.StringVar(value="Pending")
    payment_status_dropdown = ttk.Combobox(form_frame, textvariable=payment_status_var, 
                                          width=22, font=('Arial', 11))
    payment_status_dropdown['values'] = ("Pending", "Completed", "Failed", "Refunded")
    payment_status_dropdown['state'] = 'readonly'
    payment_status_dropdown.grid(row=9, column=1, pady=10, padx=(10, 0), sticky='w')
    
    def save_order():
        """Save order and automatically create corresponding payment"""
        try:
            # Get order values
            order_id = order_id_entry.get().strip()
            order_date = order_date_entry.get().strip()
            total_amount = total_amount_entry.get().strip()
            customer_id = customer_id_entry.get().strip()
            status = status_var.get()
            
            # Get payment values
            payment_method = payment_method_var.get()
            payment_date = payment_date_entry.get().strip()
            payment_status = payment_status_var.get()
            
            # Validate required fields
            if not all([order_id, customer_id, order_date, total_amount]):
                messagebox.showerror("Error", "All order fields are required!")
                return
            
            # Validate amount is a number
            try:
                amount_float = float(total_amount)
                if amount_float <= 0:
                    messagebox.showerror("Error", "Amount must be greater than 0!")
                    return
            except ValueError:
                messagebox.showerror("Error", "Amount must be a valid number!")
                return
            
            # Validate dates
            try:
                datetime.strptime(order_date, "%d/%m/%Y")
                datetime.strptime(payment_date, "%d/%m/%Y")
            except ValueError:
                messagebox.showerror("Error", "Please use DD/MM/YYYY format for dates!")
                return
            
            # Check if order ID already exists
            app.cursor.execute("SELECT OrderID FROM OrderTable WHERE OrderID = ?", (order_id,))
            if app.cursor.fetchone():
                messagebox.showerror("Error", "Order ID already exists! Please use a different ID.")
                return
            
            # Insert order into OrderTable
            app.cursor.execute("""
                INSERT INTO OrderTable (OrderID, OrderDate, TotalAmount, CustomerID, Status)
                VALUES (?, ?, ?, ?, ?)
            """, (order_id, order_date, total_amount, customer_id, status))
            
            # Generate unique payment ID
            payment_id = f"PAY_{order_id}_{datetime.now().strftime('%H%M%S')}"
            
            # Insert corresponding payment record
            app.cursor.execute("""
                INSERT INTO Payment (PaymentID, OrderID, PaymentDate, Amount, PaymentMethod, Status)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (payment_id, order_id, payment_date, total_amount, payment_method, payment_status))
            
            # Commit both transactions
            app.conn.commit()
            
            messagebox.showinfo("Success", 
                              f"✓ Order {order_id} added successfully!\n"
                              f"✓ Payment record {payment_id} created automatically!\n\n"
                              f"Order Amount: ${total_amount}\n"
                              f"Payment Method: {payment_method}")
            
            add_window.destroy()
            
            # Refresh views if they exist
            view_orders(app)
            view_payments(app)

        except Exception as e:
            app.conn.rollback()  # Rollback in case of error
            messagebox.showerror("Error", f"Failed to add order: {str(e)}")
    
    # Buttons frame
    btn_frame = tk.Frame(add_window, bg='#f0f0f0')
    btn_frame.pack(pady=25)
    
    # Save button
    save_btn = tk.Button(btn_frame, text="💾 Save Order & Payment", command=save_order,
                        bg='#4CAF50', fg='white', font=('Arial', 12, 'bold'),
                        padx=20, pady=10, relief='flat', cursor='hand2')
    save_btn.pack(side='left', padx=10)
    
    # Cancel button  
    cancel_btn = tk.Button(btn_frame, text="✖ Cancel", command=add_window.destroy,
                          bg='#f44336', fg='white', font=('Arial', 12, 'bold'),
                          padx=20, pady=10, relief='flat', cursor='hand2')
    cancel_btn.pack(side='left', padx=10)
    
    # Add hover effects
    def on_save_hover(e):
        save_btn.config(bg='#45a049')
    def on_save_leave(e):
        save_btn.config(bg='#4CAF50')
    
    def on_cancel_hover(e):
        cancel_btn.config(bg='#da190b')
    def on_cancel_leave(e):
        cancel_btn.config(bg='#f44336')
    
    save_btn.bind("<Enter>", on_save_hover)
    save_btn.bind("<Leave>", on_save_leave)
    cancel_btn.bind("<Enter>", on_cancel_hover)
    cancel_btn.bind("<Leave>", on_cancel_leave)
    
    # Focus on first entry
    order_id_entry.focus_set()

def create_simple_order_with_auto_payment(app):
    """Simple order form that automatically creates payment with defaults"""
    
    add_window = tk.Toplevel(app.root)
    add_window.title("Add New Order")
    add_window.geometry("400x350")
    add_window.resizable(False, False)
    add_window.transient(app.root)
    add_window.grab_set()
    add_window.configure(bg='#f0f0f0')
    
    # Title
    tk.Label(add_window, text="Add New Order", font=('Arial', 16, 'bold'), 
             bg='#f0f0f0').pack(pady=15)
    
    # Form frame
    form_frame = tk.Frame(add_window, bg='#f0f0f0')
    form_frame.pack(pady=10, padx=30)
    
    # Order fields only
    tk.Label(form_frame, text="Order ID:", font=('Arial', 11, 'bold'), 
             bg='#f0f0f0').grid(row=0, column=0, sticky='w', pady=8)
    order_id_entry = tk.Entry(form_frame, width=25, font=('Arial', 10))
    order_id_entry.grid(row=0, column=1, pady=8, padx=(10, 0))
    
    tk.Label(form_frame, text="Customer ID:", font=('Arial', 11, 'bold'), 
             bg='#f0f0f0').grid(row=1, column=0, sticky='w', pady=8)
    customer_id_entry = tk.Entry(form_frame, width=25, font=('Arial', 10))
    customer_id_entry.grid(row=1, column=1, pady=8, padx=(10, 0))
    
    tk.Label(form_frame, text="Date:", font=('Arial', 11, 'bold'), 
             bg='#f0f0f0').grid(row=2, column=0, sticky='w', pady=8)
    order_date_entry = tk.Entry(form_frame, width=25, font=('Arial', 10))
    order_date_entry.grid(row=2, column=1, pady=8, padx=(10, 0))
    order_date_entry.insert(0, datetime.now().strftime("%d-%m-%Y"))
    
    tk.Label(form_frame, text="Amount:", font=('Arial', 11, 'bold'), 
             bg='#f0f0f0').grid(row=3, column=0, sticky='w', pady=8)
    total_amount_entry = tk.Entry(form_frame, width=25, font=('Arial', 10))
    total_amount_entry.grid(row=3, column=1, pady=8, padx=(10, 0))
    
    tk.Label(form_frame, text="Status:", font=('Arial', 11, 'bold'), 
             bg='#f0f0f0').grid(row=4, column=0, sticky='w', pady=8)
    status_var = tk.StringVar(value="Pending")
    status_dropdown = ttk.Combobox(form_frame, textvariable=status_var, width=22)
    status_dropdown['values'] = ("Pending", "Processing", "Completed", "Cancelled")
    status_dropdown['state'] = 'readonly'
    status_dropdown.grid(row=4, column=1, pady=8, padx=(10, 0))
    
    def save_simple_order():
        try:
            order_id = order_id_entry.get().strip()
            order_date = order_date_entry.get().strip()
            total_amount = total_amount_entry.get().strip()
            customer_id = customer_id_entry.get().strip()
            status = status_var.get()
            
            if not all([order_id, customer_id, order_date, total_amount]):
                messagebox.showerror("Error", "All fields are required!")
                return
                
            # Insert order
            app.cursor.execute("""
                INSERT INTO OrderTable (OrderID, OrderDate, TotalAmount, CustomerID, Status)
                VALUES (?, ?, ?, ?, ?)
            """, (order_id, order_date, total_amount, customer_id, status))
            
            # Auto-create payment with defaults
            payment_id = f"PAY_{order_id}_{datetime.now().strftime('%H%M%S')}"
            payment_date = datetime.now().strftime("%d-%m-%Y")

            app.cursor.execute("""
                INSERT INTO Payment (PaymentID, OrderID, PaymentDate, Amount, PaymentMethod, Status)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (payment_id, order_id, payment_date, total_amount, "Cash", "Pending"))
            
            app.conn.commit()
            
            messagebox.showinfo("Success", f"Order {order_id} added with automatic payment!")
            add_window.destroy()
            
        except Exception as e:
            app.conn.rollback()
            messagebox.showerror("Error", f"Failed to add order: {e}")
    
    # Buttons
    btn_frame = tk.Frame(add_window, bg='#f0f0f0')
    btn_frame.pack(pady=20)
    
    tk.Button(btn_frame, text="Save Order", command=save_simple_order,
              bg='#4CAF50', fg='white', font=('Arial', 11, 'bold'),
              padx=20, pady=8, relief='flat').pack(side='left', padx=5)
    tk.Button(btn_frame, text="Cancel", command=add_window.destroy,
              bg='#f44336', fg='white', font=('Arial', 11, 'bold'),
              padx=20, pady=8, relief='flat').pack(side='left', padx=5)

def update_order_status(app):
        """Update order status"""
        order_id = simpledialog.askstring("Update Order", "Enter Order ID:")
        if not order_id:
            return
        
        status = simpledialog.askstring("Update Order", "Enter new status (Pending/Processing/Shipped/Delivered):")
        if not status:
            return
        
        try:
            app.cursor.execute("UPDATE OrderTable SET Status = ? WHERE OrderID = ?", (status, order_id))

            if app.cursor.rowcount > 0:
                app.conn.commit()
                messagebox.showinfo("Success", f"Order {order_id} status updated to {status}")
                view_orders(app)
            else:
                messagebox.showerror("Error", "Order ID not found!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update order: {str(e)}")

# Helpers
def get_order_entry_values(app):
    return [
        app.order_entries['OrderID'].get(),
        app.order_entries['CustomerID'].get(),
        app.order_entries['OrderDate'].get(),
        float(app.order_entries['TotalAmount'].get()),
        app.order_entries['Status'].get()
    ]
#-------------------------------Payment Management--------------------------------------------------------

# Payment management methods
def view_payments(app):
    """Display all payments"""
    for item in app.payment_tree.get_children():
        app.payment_tree.delete(item)

    try:
        app.cursor.execute("SELECT * FROM Payment")
        payments = app.cursor.fetchall()
                
        for payment in payments:
            app.payment_tree.insert('', 'end', values=payment)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch payments: {str(e)}")


#------------------------------------Custom SQL Queries-------------------------------------------------

def execute_sql_query(app):
        """Execute custom SQL query"""
        query = app.sql_text.get('1.0', tk.END).strip()
        if not query:
            messagebox.showerror("Error", "Please enter a SQL query!")
            return
        
        # Clear previous results
        for item in app.result_tree.get_children():
            app.result_tree.delete(item)

        try:
            app.cursor.execute(query)

            if query.strip().upper().startswith('SELECT'):
                # For SELECT queries, display results
                results = app.cursor.fetchall()

                if results:
                    # Set up columns based on the first result
                    columns = [description[0] for description in app.cursor.description]
                    app.result_tree['columns'] = columns
                    app.result_tree['show'] = 'headings'
                    
                    # Configure column headings
                    for col in columns:
                        app.result_tree.heading(col, text=col)
                        app.result_tree.column(col, width=100)
                    
                    # Insert data
                    for row in results:
                        app.result_tree.insert('', 'end', values=row)

                    messagebox.showinfo("Success", f"Query executed successfully! {len(results)} rows returned.")
                else:
                    messagebox.showinfo("Success", "Query executed successfully! No rows returned.")
            else:
                # For non-SELECT queries, commit changes
                app.conn.commit()
                messagebox.showinfo("Success", f"Query executed successfully! {app.cursor.rowcount} rows affected.")

        except Exception as e:
            messagebox.showerror("SQL Error", f"Query execution failed: {str(e)}")
#------------------------------------Search & Filter-------------------------------------------------
def search_customers(self, keyword):
    query = "%" + keyword + "%"
    self.cursor.execute('''
        SELECT * FROM Customer
        WHERE Name LIKE ? OR Email LIKE ? OR Phone LIKE ?
    ''', (query, query, query))
    return self.cursor.fetchall()

def filter_orders_by_status(self, status):
    self.cursor.execute("SELECT * FROM OrderTable WHERE Status = ?", (status,))
    return self.cursor.fetchall()

def filter_products_by_category(self, category):
    self.cursor.execute("SELECT * FROM Product WHERE Category = ?", (category,))
    return self.cursor.fetchall()

def generate_sales_report(app):
    """Generate a sales report and display it in result_tree"""
    query = """
        SELECT 
            o.OrderID,
            c.CustomerName || ' - ' || o.OrderID AS Customer_Order, 
            o.OrderDate,
            o.TotalAmount,
            o.Status,
            COUNT(oi.OrderItemID) AS ItemsCount
        FROM 
            OrderTable o
        JOIN 
            Customer c ON o.CustomerID = c.CustomerID
        LEFT JOIN 
            OrderItems oi ON o.OrderID = oi.OrderID
        GROUP BY o.OrderID
        ORDER BY o.OrderDate DESC
    """
    try:
        app.cursor.execute(query)
        results = app.cursor.fetchall()
        for item in app.result_tree.get_children():
            app.result_tree.delete(item)
        if results:
            columns = [description[0] for description in app.cursor.description]
            app.result_tree['columns'] = columns
            app.result_tree['show'] = 'headings'
            for col in columns:
                app.result_tree.heading(col, text=col)
                app.result_tree.column(col, width=120)
            for row in results:
                app.result_tree.insert('', 'end', values=row)
            messagebox.showinfo("Success", f"Sales report generated! {len(results)} rows returned.")
        else:
            messagebox.showinfo("Info", "No sales records found.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to generate sales report: {e}")

def generate_customer_report(app):
    """Generate a customer report and display it in result_tree"""
    query = """
        SELECT 
            c.CustomerID,
            c.CustomerName,
            c.Email,
            c.Phone,
            COUNT(o.OrderID) AS TotalOrders,
            SUM(o.TotalAmount) AS TotalSpent,
            MAX(o.OrderDate) AS LastOrderDate
        FROM 
            Customer c
        LEFT JOIN 
            OrderTable o ON c.CustomerID = o.CustomerID
        GROUP BY 
            c.CustomerID
        ORDER BY 
            TotalSpent DESC
    """
    try:
        app.cursor.execute(query)
        results = app.cursor.fetchall()

        # Clear previous results
        for item in app.result_tree.get_children():
            app.result_tree.delete(item)

        if results:
            # Setup columns
            columns = [description[0] for description in app.cursor.description]
            app.result_tree['columns'] = columns
            app.result_tree['show'] = 'headings'

            for col in columns:
                app.result_tree.heading(col, text=col)
                app.result_tree.column(col, width=120)

            # Insert data
            for row in results:
                app.result_tree.insert('', 'end', values=row)

            messagebox.showinfo("Success", f"Customer report generated! {len(results)} rows returned.")
        else:
            messagebox.showinfo("Info", "No customer records found.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to generate customer report: {e}")
