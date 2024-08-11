from customtkinter import *
from PIL import Image

apt = CTk()
apt.geometry("500x480")
apt.title("Main Menu")

CTkLabel(apt, text="UZ Pharmacy Management", font=("Arial Bold", 24), text_color="#601E88").grid(row=0, column=0, columnspan=3, pady=(20, 10))
CTkLabel(apt, text='*' * 100, font=("Arial Bold", 12), text_color="#601E88").grid(row=1, column=0, columnspan=3)
CTkLabel(apt, text='-' * 120, font=("Arial Bold", 12), text_color="#601E88").grid(row=3, column=0, columnspan=6) 

CTkLabel(apt, text="Stock Maintenance", font=("Arial Bold", 16), text_color="#601E88").grid(row=2, column=0, pady=(10, 10))
CTkButton(apt, text='New V.C.', width=100,  fg_color="#601E88", hover_color="#E44982", font=("Arial Bold", 12)).grid(row=4, column=0, pady=(5, 5))
CTkButton(apt, text='Add product to Stock', width=100, fg_color="#601E88", hover_color="#E44982", font=("Arial Bold", 12)).grid(row=5, column=0, pady=(5, 5))
CTkButton(apt, text='Delete product from Stock', width=100, fg_color="#601E88", hover_color="#E44982", font=("Arial Bold", 12)).grid(row=6, column=0, pady=(5, 5))

CTkLabel(apt, text="Access Database", font=("Arial Bold", 16), text_color="#601E88").grid(row=2, column=1, pady=(10, 10))
CTkButton(apt, text='Modify', width=100, fg_color="#601E88", hover_color="#E44982", font=("Arial Bold", 12)).grid(row=4, column=1, pady=(5, 5))
CTkButton(apt, text='Search', width=100, fg_color="#601E88", hover_color="#E44982", font=("Arial Bold", 12)).grid(row=5, column=1, pady=(5, 5))
CTkButton(apt, text='Expiry Check', width=100, fg_color="#601E88", hover_color="#E44982", font=("Arial Bold", 12)).grid(row=6, column=1, pady=(5, 5))

CTkLabel(apt, text="Handle Cash Flows", font=("Arial Bold", 16), text_color="#601E88").grid(row=2, column=2, pady=(10, 10))
CTkButton(apt, text="Check Today's Revenue", width=100, fg_color="#601E88", hover_color="#E44982", font=("Arial Bold", 12)).grid(row=5, column=2, pady=(5, 5))
CTkButton(apt, text='Billing', width=100, fg_color="#601E88", hover_color="#E44982", font=("Arial Bold", 12)).grid(row=4, column=2, pady=(5, 5))

CTkLabel(apt, text='-' * 80, font=("Arial Bold", 12), text_color="#601E88").grid(row=12, column=0, columnspan=3)
CTkButton(apt, text='Logout', fg_color="#601E88", hover_color="#E44982", font=("Arial Bold", 12)).grid(row=13, column=1)

apt.mainloop()