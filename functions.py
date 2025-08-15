from tkinter import messagebox
import sqlite3

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


# View all products
def view_products(app):
    try:
        app.cursor.execute("SELECT * FROM Product")
        rows = app.cursor.fetchall()

        # Clear old rows
        for item in app.product_tree.get_children():
            app.product_tree.delete(item)

        # Insert new rows
        for row in rows:
            app.product_tree.insert("", "end", values=row)

    except Exception as e:
        messagebox.showerror("Error", f"Failed to retrieve products: {e}")

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

#-------------------------------Customer Management--------------------------------------------------
def add_customer(self, customer_id, name, email, phone):
    try:
        self.cursor.execute('''
            INSERT INTO Customer (CustomerID, Name, Email, Phone)
            VALUES (?, ?, ?, ?)
        ''', (customer_id, name, email, phone))
        self.conn.commit()
        messagebox.showinfo("Success", "Customer added successfully.")
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Customer ID already exists.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to add customer: {e}")

def view_customers(self):
    self.cursor.execute("SELECT * FROM Customer")
    return self.cursor.fetchall()

def update_customer(self, customer_id, name=None, email=None, phone=None):
    try:
        if name:
            self.cursor.execute("UPDATE Customer SET Name = ? WHERE CustomerID = ?", (name, customer_id))
        if email:
            self.cursor.execute("UPDATE Customer SET Email = ? WHERE CustomerID = ?", (email, customer_id))
        if phone:
            self.cursor.execute("UPDATE Customer SET Phone = ? WHERE CustomerID = ?", (phone, customer_id))
        self.conn.commit()
        messagebox.showinfo("Success", "Customer updated successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to update customer: {e}")

def delete_customer(self, customer_id):
    try:
        self.cursor.execute("DELETE FROM Customer WHERE CustomerID = ?", (customer_id,))
        self.conn.commit()
        messagebox.showinfo("Success", "Customer deleted successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to delete customer: {e}")

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