import ttkbootstrap as ttk
from ttkbootstrap.constants import *

root = ttk.Window()

# default label style
l1 = ttk.Label(root, text = "primary", bootstyle="PRIMARY")
l1.pack(side=RIGHT, padx=50, pady=50)

l1 = ttk.Label(root, text = "primary", bootstyle=(INFO, "PRIMARY") )
l1.pack(side=LEFT, padx=50, pady=50)

# l2 = ttk.Label(root, text='secondary', bootstyle="SECONDARY")
# l2.pack(side=LEFT, padx=5, pady=5)

# l3 = ttk.Label(root, text='success', bootstyle="SUCCESS")
# l3.pack(side=LEFT, padx=5, pady=5)

# l4 = ttk.Label(root, text='info', bootstyle="INFO")
# l4.pack(side=LEFT, padx=5, pady=5)

# l5 = ttk.Label(root, text='warning', bootstyle="WARNING")
# l5.pack(side=LEFT, padx=5, pady=5)

# l6 = ttk.Label(root, text='danger', bootstyle="DANGER")
# l6.pack(side=LEFT, padx=5, pady=5)

# l7 = ttk.Label(root, text='light', bootstyle="LIGHT")
# l7.pack(side=LEFT, padx=5, pady=5)

# l8 = ttk.Label(root, text='dark', bootstyle="DARK")
# l8.pack(side=LEFT, padx=5, pady=5)

root.mainloop()