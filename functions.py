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