import tkinter as tk
from tkinter import ttk
import functions as func
# Import placeholder functions - you'll need to implement these
# from functions import add_product, update_product, delete_product, search_product, view_products

def create_customer_tab(app):  # Changed from self to app
    """Create customer management tab"""
    customer_frame = ttk.Frame(app.notebook)
    app.notebook.add(customer_frame, text="Customers")
    
    # Buttons frame
    btn_frame = tk.Frame(customer_frame)
    btn_frame.pack(pady=10)
    
    # Fixed button commands - using lambda functions with placeholder functions
    tk.Button(btn_frame, text="View All Customers", command=lambda: func.view_customers(app),
             bg='#4CAF50', fg='black', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
    tk.Button(btn_frame, text="Add Customer", command=lambda: func.add_customer(app),
             bg='#2196F3', fg='black', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
    tk.Button(btn_frame, text="Search Customer", command=lambda: func.search_customer(app),
             bg='#FF9800', fg='black', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
    tk.Button(btn_frame, text="Update Customer", command=lambda: func.update_customer(app),
             bg='#FF9800', fg='black', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
    tk.Button(btn_frame, text="Delete Customer", command=lambda: func.delete_customer(app),
             bg='#FF9800', fg='black', font=('Arial', 10, 'bold')).pack(side='left', padx=5)

    # Treeview for displaying customers
    app.customer_tree = ttk.Treeview(customer_frame, columns=('ID', 'Name', 'Email', 'Phone', 'Address'), show='headings')
    app.customer_tree.heading('ID', text='Customer ID')
    app.customer_tree.heading('Name', text='Name')
    app.customer_tree.heading('Email', text='Email')
    app.customer_tree.heading('Phone', text='Phone')
    app.customer_tree.heading('Address', text='Address')
    
    # Set column widths
    app.customer_tree.column('ID', width=80)
    app.customer_tree.column('Name', width=150)
    app.customer_tree.column('Email', width=200)
    app.customer_tree.column('Phone', width=120)
    app.customer_tree.column('Address', width=150)
    
    app.customer_tree.pack(fill='both', expand=True, padx=10, pady=10)
    
    # Scrollbar for customer tree
    customer_scrollbar = ttk.Scrollbar(customer_frame, orient='vertical', command=app.customer_tree.yview)
    app.customer_tree.configure(yscrollcommand=customer_scrollbar.set)
    customer_scrollbar.pack(side='right', fill='y')

def create_product_tab(app):  
    """Create product management tab"""
    product_frame = ttk.Frame(app.notebook)
    app.notebook.add(product_frame, text="Products")
    
    # Buttons frame
    btn_frame = tk.Frame(product_frame)
    btn_frame.pack(pady=10)
    
    ### CHANGED / NEW for Product Management → Popup-based like Customers
    tk.Button(btn_frame, text="View All Products", command=lambda: func.view_products(app),
             bg='#4CAF50', fg='black', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
    tk.Button(btn_frame, text="Add Product", command=lambda: func.add_product(app),
             bg='#2196F3', fg='black', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
    tk.Button(btn_frame, text="Search Product", command=lambda: func.search_product(app),
             bg='#FF9800', fg='black', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
    tk.Button(btn_frame, text="Update Product", command=lambda: func.update_product(app),
             bg='#FF9800', fg='black', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
    tk.Button(btn_frame, text="Delete Product", command=lambda: func.delete_product(app),
             bg='#FF9800', fg='black', font=('Arial', 10, 'bold')).pack(side='left', padx=5)

    # Treeview for displaying products
    app.product_tree = ttk.Treeview(product_frame, columns=('ID', 'Name', 'Price', 'Category', 'Size', 'StockQty'), show='headings')
    app.product_tree.heading('ID', text='Product ID')
    app.product_tree.heading('Name', text='Name')
    app.product_tree.heading('Price', text='Price')
    app.product_tree.heading('Category', text='Category')      
    app.product_tree.heading('Size', text='Size')
    app.product_tree.heading('StockQty', text='StockQty')
    
    app.product_tree.column('ID', width=80)
    app.product_tree.column('Name', width=150)
    app.product_tree.column('Category', width=120)
    app.product_tree.column('Price', width=100)
    app.product_tree.column('Size', width=80)
    app.product_tree.column('StockQty', width=100)
    
    app.product_tree.pack(fill='both', expand=True, padx=10, pady=10)
    
    product_scrollbar = ttk.Scrollbar(product_frame, orient='vertical', command=app.product_tree.yview)
    app.product_tree.configure(yscrollcommand=product_scrollbar.set)
    product_scrollbar.pack(side='right', fill='y')

def create_order_tab(app):  # Changed from self to app
    """Create order management tab"""
    order_frame = ttk.Frame(app.notebook)
    app.notebook.add(order_frame, text="Orders")
    
    # Buttons frame
    btn_frame = tk.Frame(order_frame)
    btn_frame.pack(pady=10)
    
    tk.Button(btn_frame, text="View All Orders", command=lambda: func.view_orders(app),
             bg='#4CAF50', fg='black', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
    tk.Button(btn_frame, text="Create Order", command=lambda: func.create_order(app),
             bg='#2196F3', fg='black', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
    tk.Button(btn_frame, text="Update Order Status", command=lambda: func.update_order_status(app),
             bg='#FF9800', fg='black', font=('Arial', 10, 'bold')).pack(side='left', padx=5)

    # Treeview for displaying orders
    app.order_tree = ttk.Treeview(order_frame, columns=('OrderID', 'Date', 'Amount', 'CustomerID', 'Status'), show='headings')
    app.order_tree.heading('OrderID', text='Order ID')
    app.order_tree.heading('Date', text='Order Date')
    app.order_tree.heading('Amount', text='Total Amount')
    app.order_tree.heading('CustomerID', text='Customer ID')
    app.order_tree.heading('Status', text='Status')
    
    # Set column widths
    app.order_tree.column('OrderID', width=100)
    app.order_tree.column('Date', width=120)
    app.order_tree.column('Amount', width=100)
    app.order_tree.column('CustomerID', width=100)
    app.order_tree.column('Status', width=100)
    
    app.order_tree.pack(fill='both', expand=True, padx=10, pady=10)

def create_payment_tab(app):  # Changed from self to app
    """Create payment management tab"""
    payment_frame = ttk.Frame(app.notebook)
    app.notebook.add(payment_frame, text="Payments")
    
    # Buttons frame
    btn_frame = tk.Frame(payment_frame)
    btn_frame.pack(pady=10)
    
    tk.Button(btn_frame, text="View All Payments", command=lambda: func.view_payments(app),
             bg='#4CAF50', fg='black', font=('Arial', 10, 'bold')).pack(side='left', padx=5)

    # Treeview for displaying payments
    app.payment_tree = ttk.Treeview(payment_frame, columns=('PaymentID', 'OrderID', 'Amount', 'Date', 'Method', 'Status'), show='headings')
    app.payment_tree.heading('PaymentID', text='Payment ID')
    app.payment_tree.heading('OrderID', text='Order ID')
    app.payment_tree.heading('Amount', text='Amount')
    app.payment_tree.heading('Date', text='Payment Date')
    app.payment_tree.heading('Method', text='Payment Method')
    app.payment_tree.heading('Status', text='Payment Status')

    # Set column widths
    app.payment_tree.column('PaymentID', width=100)
    app.payment_tree.column('OrderID', width=100)
    app.payment_tree.column('Amount', width=120)
    app.payment_tree.column('Date', width=100)
    app.payment_tree.column('Method', width=100)
    app.payment_tree.column('Status', width=100)
    
    app.payment_tree.pack(fill='both', expand=True, padx=10, pady=10)

def create_sql_tab(app):
        """Create SQL query execution tab"""
        sql_frame = ttk.Frame(app.notebook)
        app.notebook.add(sql_frame, text="SQL Queries")

        # SQL input area
        tk.Label(sql_frame, text="Enter SQL Query:", font=('Arial', 12, 'bold')).pack(pady=10)

        app.sql_text = tk.Text(sql_frame, height=8, width=80, font=('Consolas', 10))
        app.sql_text.pack(padx=10, pady=5)
        
        # Buttons
        btn_frame = tk.Frame(sql_frame)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Execute Query", command=lambda: func.execute_sql_query(app),
                 bg='#4CAF50', fg='black', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Clear", command=lambda: app.sql_text.delete('1.0', tk.END),
                 bg='#f44336', fg='black', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        
        # Results area
        tk.Label(sql_frame, text="Query Results:", font=('Arial', 12, 'bold')).pack(pady=(20, 5))

        app.result_tree = ttk.Treeview(sql_frame, show='headings')
        app.result_tree.pack(fill='both', expand=True, padx=10, pady=5)

def create_report_tab(app):
        """Create Report tab"""
        report_frame = ttk.Frame(app.notebook)
        app.notebook.add(report_frame, text="Generate Report")
        
        # Buttons
        btn_frame = tk.Frame(report_frame)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Generate Sales Report", command=lambda: func.generate_sales_report(app),
                 bg='#36b1f4', fg='black', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Generate Customer Report", command=lambda: func.generate_customer_report(app),
                 bg="#36b1f4", fg='black', font=('Arial', 10, 'bold')).pack(side='left', padx=5)

        app.result_tree = ttk.Treeview(report_frame, show='headings')
        app.result_tree.pack(fill='both', expand=True, padx=10, pady=5)