from tkinter import *
import ttkbootstrap as ttk
from datetime import date

root = ttk.Window(themename='superhero')
root.title("Frame")
root.geometry('500x400')

def speak():
    pass

my_frame = ttk.Frame(root, bootstyle="light")
my_frame.pack(pady=40)

my_entry = ttk.Entry(my_frame, bootstyle="success", 
                     font=("Helvetica",18))
my_entry.pack(pady=20, padx=20)

my_button = ttk.Button(my_frame, text="Click Me!", bootstyle="dark", command=speak)
my_button.pack(pady=20, padx=20)

my_label = ttk.Label(root, text = "Hello CE !", font=("Helvetica",14), bootstyle="inverse success")
my_label.pack(pady=20)

root.mainloop()

