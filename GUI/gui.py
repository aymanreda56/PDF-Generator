import customtkinter as ctk

def submit_text():
    text = textbox.get()
    print("Text entered:", text)
    # You can perform any action with the entered text here

root = ctk.CTk()
root.title("Custom Tkinter App")
root.geometry("400x300")  # Set window size

label = ctk.CTkLabel(root, text="Enter your text:")
label.pack(pady=10)

textbox = ctk.CTkEntry(root, font=("Arial", 12), width=300)
textbox.pack(pady=10)

submit_button = ctk.CTkButton(root, text="Submit", command=submit_text)
submit_button.pack(pady=10)

root.mainloop()