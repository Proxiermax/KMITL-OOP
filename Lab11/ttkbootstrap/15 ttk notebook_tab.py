from tkinter import *
import ttkbootstrap as ttk

root = ttk.Window(themename='superhero')
root.title("Notebook Tab")
root.geometry('400x300')

my_notebook = ttk.Notebook(root, bootstyle="info")
my_notebook.pack(pady=20)

tab1=ttk.Frame(my_notebook)
tab2=ttk.Frame(my_notebook)

my_label = Label(tab1, text="Awesome Label!", font=("Helvetica",14))
my_label.pack(pady=20)
my_text = Text(tab1, width=70, height=10)
my_label.pack(padx=10, pady=20)
my_button = ttk.Button(tab1, text="Click Me!", bootstyle="danger outline")
my_button.pack(pady=20)

my_notebook.add(tab1, text="Tab One")
my_notebook.add(tab2, text="Tab Two")

root.mainloop()

