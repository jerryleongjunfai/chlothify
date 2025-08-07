from tkinter import messagebox



# ---------------PRODUCT MANAGEMENT------------------
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
