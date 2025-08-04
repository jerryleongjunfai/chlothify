import sqlite3
import tkinter as tk

# Create the main window
root = tk.Tk()
root.title("Clothify GUI")
root.geometry("300x200")  # width x height

# Add a label
label = tk.Label(root, text="Welcome to Clothify!")
label.pack(pady=20)

# Add a button
def on_click():
    label.config(text="Button Clicked!")

button = tk.Button(root, text="Click Me", command=on_click)
button.pack()

# Start the GUI loop
root.mainloop()

# Connect to SQLite (creates a new file if not exists)
conn = sqlite3.connect("store.db")
cursor = conn.cursor()

