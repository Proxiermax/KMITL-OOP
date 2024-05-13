from tkinter import *
import ttkbootstrap as ttk

root = ttk.Window(themename='superhero')
root.title("Meter widget")
root.geometry('400x500')

def update_label():
    my_label.config(text=my_meter.amountusedvar.get())

my_meter = ttk.Meter(root, bootstyle="danger", 
                     subtext="Drag Me!", 
                     interactive=True, 
                     textleft="$", textright="%",
                     metertype="full",  # try semi
                     stripethickness=10,# แสดงแถบในวงกลม
                     metersize=200, padding=50,
                     amountused=20,     # ค่าเริ่มต้น  
                     amounttotal=100,   # ค่ามากสุด
                     subtextstyle="success"
                     )
my_meter.pack(pady=20)

my_label = ttk.Label(root, text=my_meter.amountusedvar.get())
my_label.pack(pady=10)

update_label()  # Set the initial label text
my_meter.amountusedvar.trace_add('write', lambda *args: update_label())

root.mainloop()

