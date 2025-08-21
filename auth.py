import tkinter as tk
import functions
import main as main
from tkinter import messagebox

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
            app = main.ClothifyGUI(main_root)
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
    login_btn.pack(pady=(10, 20))

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