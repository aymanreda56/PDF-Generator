import customtkinter as ctk
import re
from datetime import date


first_window_root = ctk.CTk()
first_window_root.title("Secretary Assistant")
first_window_root.geometry("1000x600")  # Set window size

Big_Label = ctk.CTkLabel(first_window_root, text="Secretary Assistant", font=('cooper black gothic', 50, 'bold'))
Big_Label.pack()



first_window_root.mainloop()