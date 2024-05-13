from tkinter import *
import ttkbootstrap as ttk

root = ttk.Window(themename='superhero')
root.title("Menu Button")
root.geometry('400x300')

def stuff(x):
    my_menu.config(bootstyle=x)
    my_label.config(text=x)

my_menu = ttk.Menubutton(root, bootstyle="warning", text="Hello")
my_menu.pack(pady=50)

inside_menu = ttk.Menu(my_menu)

# add item to menu
item_var = StringVar()
for x in ['primary','secondary','danger', 'info', 'outline primary', 
          'outline secondary', 'outline danger', 'outline info']:
    inside_menu.add_radiobutton(label=x, variable=item_var, command=lambda x=x: stuff(x))

# associate the inside menu with menubutton
my_menu['menu'] = inside_menu

my_label = ttk.Label(root, text="")
my_label.pack(pady=40)

root.mainloop()

