import tkinter as tk
from tkinter import ttk

root = tk.Tk()

def create_table():
    data = [1, 2, 3, 4, 5]
    for i, item in enumerate(data):
        tree.insert("", "end", values=(i+1, item))

root = tk.Tk()
root.title("Table Creation Example")
root.geometry("400x300")

# Create a Treeview widget
tree = ttk.Treeview(root, columns=("Index", "Value"), show="headings")
tree.heading("Index", text="Index")
tree.heading("Value", text="Value")
tree.pack(pady=10)

# Create a button to trigger table creation
button = tk.Button(root, text="Create Table", command=create_table)
button.pack()

root.mainloop()
