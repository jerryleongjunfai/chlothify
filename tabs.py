import tkinter as tk
from tkinter import ttk

from functions import add_product, update_product, delete_product, search_product, view_products  #functions from product tab

def create_customer_tab(self):
        """Create customer management tab"""
        customer_frame = ttk.Frame(self.notebook)
        self.notebook.add(customer_frame, text="Customers")
        
        # Buttons frame
        btn_frame = tk.Frame(customer_frame)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="View All Customers", command=self,
                 bg='#4CAF50', fg='black', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Add Customer", command=self,
                 bg='#2196F3', fg='black', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Search Customer", command=self,
                 bg='#FF9800', fg='black', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        
        # Treeview for displaying customers
        self.customer_tree = ttk.Treeview(customer_frame, columns=('ID', 'Name', 'Email', 'Phone', 'Address'), show='headings')
        self.customer_tree.heading('ID', text='Customer ID')
        self.customer_tree.heading('Name', text='Name')
        self.customer_tree.heading('Email', text='Email')
        self.customer_tree.heading('Phone', text='Phone')
        self.customer_tree.heading('Address', text='Address')
        
        # Set column widths
        self.customer_tree.column('ID', width=80)
        self.customer_tree.column('Name', width=150)
        self.customer_tree.column('Email', width=200)
        self.customer_tree.column('Phone', width=120)
        self.customer_tree.column('Address', width=150)
        
        self.customer_tree.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Scrollbar for customer tree
        customer_scrollbar = ttk.Scrollbar(customer_frame, orient='vertical', command=self.customer_tree.yview)
        self.customer_tree.configure(yscrollcommand=customer_scrollbar.set)
        customer_scrollbar.pack(side='right', fill='y')

def create_product_tab(self):
        """Create product management tab"""
        product_frame = ttk.Frame(self.notebook)
        self.notebook.add(product_frame, text="Products")
        
        # Buttons frame
        btn_frame = tk.Frame(product_frame)
        btn_frame.pack(pady=10)

        self.product_entries = {}  
        fields = ['ProductID', 'ProductName', 'Price', 'Category', 'Size', 'StockQty']  

        for i, field in enumerate(fields): 
                lbl = tk.Label(product_frame, text=field + ":") 
                lbl.pack()  
                entry = tk.Entry(product_frame)  
                entry.pack()  
                self.product_entries[field] = entry  
        
        tk.Button(btn_frame, text="View All Products", command=lambda: view_products(self),
                 bg='#4CAF50', fg='black', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Add Product", command=lambda: add_product(self),
                 bg='#2196F3', fg='black', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Update Stock", command=lambda: update_product(self),
                 bg='#FF9800', fg='black', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Delete Product", command=lambda: delete_product(self),
              bg='#f44336', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5)  
        tk.Button(btn_frame, text="Search Product", command=lambda: search_product(self),
              bg='#9C27B0', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=5)  
        
        # Treeview for displaying products
        self.product_tree = ttk.Treeview(product_frame, columns=('ProductID', 'ProductName', 'ProductPrice', 'Category', 'Size', 'StockQty'), show='headings')
        self.product_tree.heading('ProductID', text='Product ID')
        self.product_tree.heading('ProductName', text='Product Name')
        self.product_tree.heading('ProductPrice', text='Price ($)')
        self.product_tree.heading('Category', text='Category')
        self.product_tree.heading('Size', text='Size')
        self.product_tree.heading('StockQty', text='StockQty')
        self.product_tree.pack(fill='both', expand=True, padx=10, pady=10)

def create_order_tab(self):
        """Create order management tab"""
        order_frame = ttk.Frame(self.notebook)
        self.notebook.add(order_frame, text="Orders")
        
        # Buttons frame
        btn_frame = tk.Frame(order_frame)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="View All Orders", command=self,
                 bg='#4CAF50', fg='black', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Create Order", command=self,
                 bg='#2196F3', fg='black', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Update Order Status", command=self,
                 bg='#FF9800', fg='black', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        
        # Treeview for displaying orders
        self.order_tree = ttk.Treeview(order_frame, columns=('OrderID', 'CustomerID', 'Date', 'Amount', 'Status'), show='headings')
        self.order_tree.heading('OrderID', text='Order ID')
        self.order_tree.heading('CustomerID', text='Customer ID')
        self.order_tree.heading('Date', text='Order Date')
        self.order_tree.heading('Amount', text='Total Amount')
        self.order_tree.heading('Status', text='Status')
        
        self.order_tree.pack(fill='both', expand=True, padx=10, pady=10)

def create_payment_tab(self):
        """Create payment management tab"""
        payment_frame = ttk.Frame(self.notebook)
        self.notebook.add(payment_frame, text="Payments")
        
        # Buttons frame
        btn_frame = tk.Frame(payment_frame)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="View All Payments", command=self,
                 bg='#4CAF50', fg='black', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Process Payment", command=self,
                 bg='#2196F3', fg='black', font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        
        # Treeview for displaying payments
        self.payment_tree = ttk.Treeview(payment_frame, columns=('PaymentID', 'OrderID', 'Date', 'Amount', 'Method', 'Status'), show='headings')
        self.payment_tree.heading('PaymentID', text='Payment ID')
        self.payment_tree.heading('OrderID', text='Order ID')
        self.payment_tree.heading('Date', text='Payment Date')
        self.payment_tree.heading('Amount', text='Amount')
        self.payment_tree.heading('Method', text='Method')
        self.payment_tree.heading('Status', text='Status')
        
        self.payment_tree.pack(fill='both', expand=True, padx=10, pady=10)

