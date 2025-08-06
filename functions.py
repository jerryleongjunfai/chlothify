import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

#Connect to database
def connect_db():
    conn = sqlite3.connect("store.db")
    cursor = conn.cursor()
    return conn, cursor

#Function to create Product Management Tab under Clothify Store Management System
def create_product_tab(tab):
    labels = ["Product ID", "Product Name", "Category", "Price", "Size", "StockQty"]
    entries = {}

    for i, label in enumerate(labels):
        tk.Label(tab, text=label).grid(row=i, column=0, padx=10, pady=5, sticky="e")
        entry = tk.Entry(tab)
        entry.grid(row=i, column=1, padx=10, pady=5)
        entries[label] = entry

    
    tk.Button(tab, text="Add Product", command=lambda: add_product(entries)).grid(row=0, column=2, padx=10)
    tk.Button(tab, text="Update Product", command=lambda: update_product(entries)).grid(row=1, column=2, padx=10)
    tk.Button(tab, text="Delete Product", command=lambda: delete_product(entries["Product ID"])).grid(row=2, column=2, padx=10)
    tk.Button(tab, text="Search Product", command=lambda: search_product(entries["Product ID"], entries)).grid(row=3, column=2, padx=10)
    tk.Button(tab, text="View All Products", command=lambda: view_product_list(tree)).grid(row=4, column=2, padx=10)

    
    global tree
    tree = ttk.Treeview(tab, columns=labels, show="headings")
    for col in labels:
        tree.heading(col, text=col)
        tree.column(col, width=100)
    tree.grid(row=7, column=0, columnspan=3, padx=10, pady=20)

#Product management functions
def add_product(entries):
    data = {key: entry.get() for key, entry in entries.items()}

    try:
        conn, cursor = connect_db()
        cursor.execute("""
            INSERT INTO Product (ProductID, ProductName, Category, Price, Description, StockQuantity)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            data["Product ID"],
            data["Product Name"],
            data["Category"],
            float(data["Price"]),
            data["Size"],
            int(data["StockQty"])
        ))
        conn.commit()
        messagebox.showinfo("Success", "Product added successfully!")
        view_product_list(tree)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to add product: {e}")
    finally:
        conn.close()

def update_product(entries):
    data = {key: entry.get() for key, entry in entries.items()}

    try:
        conn, cursor = connect_db()
        cursor.execute("""
            UPDATE Product
            SET ProductName=?, Category=?, Price=?, Description=?, StockQuantity=?
            WHERE ProductID=?
        """, (
            data["Product Name"],
            data["Category"],
            float(data["Price"]),
            data["Size"],
            int(data["StockQty"]),
            data["Product ID"]
        ))
        conn.commit()
        if cursor.rowcount == 0:
            messagebox.showwarning("Update", "No product found with that ID.")
        else:
            messagebox.showinfo("Success", "Product updated successfully!")
            view_product_list(tree)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to update product: {e}")
    finally:
        conn.close()

def delete_product(product_id_entry):
    product_id = product_id_entry.get()
    if not product_id:
        messagebox.showwarning("Delete", "Enter Product ID to delete.")
        return

    try:
        conn, cursor = connect_db()
        cursor.execute("DELETE FROM Product WHERE ProductID=?", (product_id,))
        conn.commit()
        if cursor.rowcount == 0:
            messagebox.showwarning("Delete", "No product found with that ID.")
        else:
            messagebox.showinfo("Success", "Product deleted successfully!")
            view_product_list(tree)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to delete product: {e}")
    finally:
        conn.close()

def search_product(product_id_entry, entries):
    product_id = product_id_entry.get()

    try:
        conn, cursor = connect_db()
        cursor.execute("SELECT * FROM Product WHERE ProductID=?", (product_id,))
        product = cursor.fetchone()

        if product:
            keys = ["Product ID", "Product Name", "Category", "Price", "Size", "StockQty"]
            for i, key in enumerate(keys):
                entries[key].delete(0, tk.END)
                entries[key].insert(0, str(product[i]))
        else:
            messagebox.showinfo("Search", "Product not found.")
    except Exception as e:
        messagebox.showerror("Error", f"Search failed: {e}")
    finally:
        conn.close()

def view_product_list(tree):
    for item in tree.get_children():
        tree.delete(item)

    try:
        conn, cursor = connect_db()
        cursor.execute("SELECT ProductID, ProductName, Category, Price, Description, StockQuantity FROM Product")
        for row in cursor.fetchall():
            tree.insert("", tk.END, values=row)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load product list: {e}")
    finally:
        conn.close()

