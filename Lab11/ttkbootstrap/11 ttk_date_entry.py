from tkinter import *
import ttkbootstrap as ttk
from datetime import date

root = ttk.Window(themename='superhero')
root.title("Date Entry")
root.geometry('600x500')

def datey():
    my_label.config(text=f"You picked: {my_date.entry.get()}")


my_date = ttk.DateEntry(root, bootstyle="danger", startdate=date.today())
my_date.pack(pady=30)

my_button = ttk.Button(root, text="Get Date", bootstyle="danger, outline", command=datey)
my_button.pack(pady=20)

my_label = ttk.Label(root, text = "You Picked: ")
my_label.pack(pady=20)

root.mainloop()


