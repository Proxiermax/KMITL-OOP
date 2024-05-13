from tkinter import *
import ttkbootstrap as ttk

root = ttk.Window(themename='superhero')
root.title("Progress Bar")
root.geometry('600x500')

def starter():
    my_gauge.start()
def stoper():
    my_gauge.stop()
def incrementer():
    my_gauge.step(10)

my_gauge = ttk.Floodgauge(root, bootstyle="success", font=("Helvetica",14),mask="Pos: {}%",maximum=80, 
                          orient="horizontal",value=0, mode="determinate")  # try indeterminate
my_gauge.pack(pady=50,fill=X,padx=20)

start_button = ttk.Button(root, text="Start", bootstyle="danger, outline", command=starter)
start_button.pack(pady=20)

stop_button = ttk.Button(root, text="Stop", bootstyle="danger, outline", command=stoper)
stop_button.pack(pady=20)

increment_button = ttk.Button(root, text="Increment", bootstyle="danger, outline", command=incrementer)
increment_button.pack(pady=20)

root.mainloop()


