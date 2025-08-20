from tkinter import messagebox, simpledialog
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
# Add a new product
def add_product(app):
    try:
        values = get_product_entry_values(app)
        if any(v == "" for v in values):
            messagebox.showerror("Input Error", "All fields must be filled.")
            return

        app.cursor.execute("""
            INSERT INTO Product (ProductID, ProductName, ProductPrice, Category, Size, StockQty)
            VALUES (?, ?, ?, ?, ?, ?)
        """, values)
        app.conn.commit()
        messagebox.showinfo("Success", "Product added successfully!")
        view_products(app)

    except Exception as e:
        messagebox.showerror("Error", f"Failed to add product: {e}")


# Update existing product
def update_product(app):
    try:
        values = get_product_entry_values(app)
        app.cursor.execute("""
            UPDATE Product
            SET ProductName = ?, ProductPrice = ?, Category = ?, Size = ?, StockQty = ?
            WHERE ProductID = ?
        """, (values[1], values[2], values[3], values[4], values[5], values[0]))
        if app.cursor.rowcount == 0:
            messagebox.showwarning("Not Found", "No product found with that ID.")
        else:
            app.conn.commit()
            messagebox.showinfo("Success", "Product updated successfully!")
            view_products(app)

    except Exception as e:
        messagebox.showerror("Error", f"Failed to update product: {e}")


# Delete a product
def delete_product(app):
    product_id = app.product_entries['ProductID'].get()
    if not product_id:
        messagebox.showerror("Input Error", "Please enter a Product ID to delete.")
        return
    try:
        app.cursor.execute("DELETE FROM Product WHERE ProductID = ?", (product_id,))
        if app.cursor.rowcount == 0:
            messagebox.showwarning("Not Found", "No product found with that ID.")
        else:
            app.conn.commit()
            messagebox.showinfo("Success", "Product deleted successfully!")
            view_products(app)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to delete product: {e}")


# Search a product by ID
def search_product(app):
    product_id = app.product_entries['ProductID'].get()
    if not product_id:
        messagebox.showerror("Input Error", "Please enter a Product ID to search.")
        return
    try:
        app.cursor.execute("SELECT * FROM Product WHERE ProductID = ?", (product_id,))
        row = app.cursor.fetchone()
        if row:
            fill_product_entries(app, row)
        else:
            messagebox.showinfo("Not Found", "No product found with that ID.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to search product: {e}")

# Product management methods
def view_products(app):
        """Display all products"""
        for item in app.product_tree.get_children():
            app.product_tree.delete(item)
        
        try:
            # Check which table exists (Products or Product)
            app.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND (name='Products' OR name='Product')")
            product_table = app.cursor.fetchone()

            if product_table:
                table_name = product_table[0]
                app.cursor.execute(f"SELECT * FROM {table_name}")
                products = app.cursor.fetchall()
                
                for product in products:
                    app.product_tree.insert('', 'end', values=product)
            else:
                messagebox.showinfo("Info", "No product table found. Please add some products first.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch products: {str(e)}")

#Clear all data in entries :D
def clear_product_entries(app):
    for entry in app.product_entries.values():
        entry.delete(0, 'end')
# Helpers
def get_product_entry_values(app):
    return [
        app.product_entries['ProductID'].get(),
        app.product_entries['ProductName'].get(),
        float(app.product_entries['ProductPrice'].get()),
        app.product_entries['Category'].get(),
        app.product_entries['Size'].get(),
        int(app.product_entries['StockQty'].get())
    ]

def fill_product_entries(app, row):
    keys = ['ProductID', 'ProductName', 'ProductPrice', 'Category', 'Size', 'StockQty']
    for i, key in enumerate(keys):
        app.product_entries[key].delete(0, 'end')
        app.product_entries[key].insert(0, row[i])

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
        """Add a new order"""
        def save_order():
            try:
                order_id = order_id_entry.get()
                order_date = order_date_entry.get()
                total_amount = total_amount_entry.get()
                customer_id = customer_id_entry.get()
                status = status_entry.get()

                if not all([customer_id, order_date, total_amount, status]):
                    messagebox.showerror("Error", "All fields are required!")
                    return
                
                app.cursor.execute("""
                    INSERT INTO OrderTable (OrderID, OrderDate, TotalAmount, CustomerID, Status)
                    VALUES (?, ?, ?, ?, ?)
                """, (order_id, order_date, total_amount, customer_id, status))

                app.conn.commit()
                messagebox.showinfo("Success", "Order added successfully!")
                add_window.destroy()
                view_customers(app)  # Refresh the view

            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Order ID already exists!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add order: {str(e)}")
        
        # Create add customer window
        add_window = tk.Toplevel(app.root)
        add_window.title("Add New Order")
        add_window.geometry("400x500")
        
        # Form fields
        tk.Label(add_window, text="Order ID:").pack(pady=5)
        order_id_entry = tk.Entry(add_window, width=30)
        order_id_entry.pack(pady=5)
        
        tk.Label(add_window, text="Date:").pack(pady=5)
        order_date_entry = tk.Entry(add_window, width=30)
        order_date_entry.pack(pady=5)

        tk.Label(add_window, text="Amount:").pack(pady=5)
        total_amount_entry = tk.Entry(add_window, width=30)
        total_amount_entry.pack(pady=5)

        tk.Label(add_window, text="Customer ID:").pack(pady=5)
        customer_id_entry = tk.Entry(add_window, width=30)
        customer_id_entry.pack(pady=5)

        tk.Label(add_window, text="Status:").pack(pady=5)
        status_entry = tk.Entry(add_window, width=30)
        status_entry.pack(pady=5)

        tk.Button(add_window, text="Save Order", command=save_order,
                 bg='#4CAF50', fg='black', font=('Arial', 15, 'bold')).pack(pady=20)

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


#-------------------------------Stock Management--------------------------------------------------------
def adjust_stock(self, product_id, quantity_change):
    try:
        self.cursor.execute("UPDATE Product SET StockQuantity = StockQuantity + ? WHERE ProductID = ?", 
                            (quantity_change, product_id))
        self.conn.commit()
        messagebox.showinfo("Success", "Stock adjusted.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to adjust stock: {e}")

def check_stock_level(self, product_id):
    self.cursor.execute("SELECT StockQuantity FROM Product WHERE ProductID = ?", (product_id,))
    result = self.cursor.fetchone()
    return result[0] if result else None

def get_low_stock_items(self, threshold=5):
    self.cursor.execute("SELECT * FROM Product WHERE StockQuantity <= ?", (threshold,))
    return self.cursor.fetchall()

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

def generate_sales_report(self, start_date=None, end_date=None):
    """Generate a sales report with optional date range filtering"""
    try:
        query = """
            SELECT 
                o.OrderID,
                o.OrderDate,
                o.TotalAmount,
                o.Status,
                c.Name AS CustomerName,
                COUNT(oi.OrderItemID) AS ItemsCount
            FROM 
                OrderTable o
            JOIN 
                Customer c ON o.CustomerID = c.CustomerID
            LEFT JOIN 
                OrderItems oi ON o.OrderID = oi.OrderID
        """
        
        params = []
        if start_date and end_date:
            query += " WHERE o.OrderDate BETWEEN ? AND ?"
            params.extend([start_date, end_date])
        elif start_date:
            query += " WHERE o.OrderDate >= ?"
            params.append(start_date)
        elif end_date:
            query += " WHERE o.OrderDate <= ?"
            params.append(end_date)
            
        query += " GROUP BY o.OrderID ORDER BY o.OrderDate DESC"
        
        self.cursor.execute(query, params)
        return self.cursor.fetchall()
        
    except Exception as e:
        messagebox.showerror("Error", f"Failed to generate sales report: {e}")
        return []

def generate_customer_report(self):
    """Generate a report of customer purchasing activity"""
    try:
        self.cursor.execute("""
            SELECT 
                c.CustomerID,
                c.Name,
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
        """)
        return self.cursor.fetchall()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to generate customer report: {e}")
        return []

def top_selling_products(self, limit=10, days=None):
    """Get top selling products with optional time period filtering"""
    try:
        query = """
            SELECT 
                p.ProductID,
                p.ProductName,
                p.Category,
                SUM(oi.Quantity) AS TotalSold,
                SUM(oi.Quantity * oi.UnitPrice) AS TotalRevenue
            FROM 
                OrderItems oi
            JOIN 
                Product p ON oi.ProductID = p.ProductID
            JOIN 
                OrderTable o ON oi.OrderID = o.OrderID
        """
        
        params = []
        if days:
            query += " WHERE o.OrderDate >= date('now', ?)"
            params.append(f"-{days} days")
            
        query += """
            GROUP BY 
                p.ProductID
            ORDER BY 
                TotalSold DESC
            LIMIT ?
        """
        params.append(limit)
        
        self.cursor.execute(query, params)
        return self.cursor.fetchall()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to get top selling products: {e}")
        return []

def monthly_revenue_chart(self, months=12):
    """Generate monthly revenue data for charting"""
    try:
        self.cursor.execute("""
            SELECT 
                strftime('%Y-%m', OrderDate) AS Month,
                SUM(TotalAmount) AS Revenue
            FROM 
                OrderTable
            WHERE 
                OrderDate >= date('now', 'start of month', ?)
                AND Status = 'Completed'
            GROUP BY 
                strftime('%Y-%m', OrderDate)
            ORDER BY 
                Month
        """, (f"-{months-1} months",))
        
        results = self.cursor.fetchall()
        
        # Format results for charting
        months = []
        revenues = []
        for row in results:
            months.append(row[0])
            revenues.append(row[1])
            
        return months, revenues
    except Exception as e:
        messagebox.showerror("Error", f"Failed to generate revenue chart data: {e}")
        return [], []