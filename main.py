import customtkinter as ctk
from PIL import Image, ImageTk
import ctypes

from functional_components import *
from rendering_components import *

import tkinter as tk

def show_context_menu(event, component):
    TransactionWindow(root, component, refresh_list)

# setup ctk main window
ctk.set_appearance_mode("dark")
root = ctk.CTk()
root.geometry("1000x600")


root.iconbitmap("icons/logo.ico")
root.overrideredirect(True)
hwnd = ctypes.windll.user32.GetParent(root.winfo_id())

ctypes.windll.user32.SetWindowLongW(hwnd, -16, 0x10000000 | 0x40000000)
ctypes.windll.user32.SetWindowLongW(hwnd, -20, ctypes.windll.user32.GetWindowLongW(hwnd, -20) & ~0x80)
ctypes.windll.user32.SetWindowLongW(hwnd, -20, ctypes.windll.user32.GetWindowLongW(hwnd, -20) | 0x00040000)
ctypes.windll.user32.ShowWindow(hwnd, 5)

# main window binding
def start_move(event):
    root.x = event.x
    root.y = event.y

def do_move(event):
    deltax = event.x - root.x
    deltay = event.y - root.y
    root.geometry(f"+{root.winfo_x() + deltax}+{root.winfo_y() + deltay}")

def minimize_window():
    root.update_idletasks()
    ctypes.windll.user32.ShowWindow(hwnd, 6)

def maximize_window():
    if root.state() == "normal":
        root.state("zoomed")
    else:
        root.state("normal")





financial_components = [
    Savings("Hypotéka", 25000, "icons/house.png", 0),
    Savings("Svadba", 6000, "icons/wedding.png", 0),
    Savings("Prsteň", 900, "icons/ring.png", 0),
    Budget("Spotreba", "icons/money.png", 0),
    Budget("Dlžia mi", "icons/money.png", 0),
]

# create main components
title_bar = Bar(root, maximize_window, minimize_window, start_move, do_move, "Cash Flow", "icons/logo.png")
scroll_frame = ScrollableFrame(root, 580, 350)

trans1 = Transaction(5875.0, TransactionType.INCOME, datetime.now(), "Transakcia č. 1")
trans2 = Transaction(557.0, TransactionType.EXPENSE, datetime.now(), "Transakcia č. 2")
financial_components[0].add_transaction(trans1)
financial_components[0].add_transaction(trans2)

def show_details(component):
    # 1. Clear the frame
    for widget in scroll_frame.winfo_children():
        widget.destroy()

    # 2. Back Button (Top Left)
    back_btn = ctk.CTkButton(scroll_frame, text="◄ Back", width=80, 
                             fg_color="transparent", hover_color="#2b2b2b",
                             border_color="#72bd39", border_width=1, font=("Courier New", 18, "bold"),
                             command=refresh_list)
    back_btn.pack(anchor="w", padx=30, pady=10)

    # 3. Main Detail Container
    # We use a frame so we can use grid inside it independently
    detail_container = ctk.CTkFrame(scroll_frame, fg_color="transparent")
    detail_container.pack(fill="x", padx=20, pady=10)
    
    # Configure columns: Column 0 (Text) expands, Column 1 (Ring) stays fixed
    detail_container.columnconfigure(0, weight=1)
    detail_container.columnconfigure(1, weight=0)

    # --- LEFT SIDE: TEXT INFO (Column 0) ---
    text_info_frame = ctk.CTkFrame(detail_container, fg_color="transparent")
    text_info_frame.grid(row=0, column=0, sticky="nsw", padx=10)

    # Component Name
    name_label = ctk.CTkLabel(text_info_frame, text=component.name, 
                              font=("Courier New", 50, "bold"), text_color="#72bd39")
    name_label.pack(anchor="w")

    
    if isinstance(component, Savings):
        amt_text = f"{component.current_amount}/{component.target_amount}€"
    else:
        amt_text = f"{component.current_amount}€"
        
    amount_label = ctk.CTkLabel(text_info_frame, text=amt_text, 
                                font=("Courier New", 18), text_color="#619f31")
    amount_label.pack(anchor="w", pady=(15, 40))

    


    # --- RIGHT SIDE: PERCENTAGE RING (Column 1) ---
    if isinstance(component, Savings):
        ring_frame = ctk.CTkFrame(detail_container, fg_color="transparent")
        ring_frame.grid(row=0, column=1, padx=20, sticky="ne")

        size = 120
        thickness = 8
        percent = component.calculate_percent()
        
        canvas = ctk.CTkCanvas(ring_frame, width=size, height=size,
                               bg="#2b2b2b", highlightthickness=0)
        canvas.pack()
        
        # Background circle
        canvas.create_oval(thickness, thickness, size-thickness, size-thickness,
                           outline="#131313", width=thickness)
        # Progress arc
        canvas.create_arc(thickness, thickness, size-thickness, size-thickness,
                          start=90, extent=360 * (percent / 100),
                          outline="#72bd39", width=thickness, style="arc")
        # Center Text
        canvas.create_text(size/2, size/2, text=f"{percent:.0f}%", 
                           fill="#72bd39", font=("Courier New", 22, "bold"))

    # 4. Transactions List below
    ctk.CTkLabel(scroll_frame, text="Recent Transactions", font=("Courier New", 18, "bold")).pack(pady=(30, 10))
    
    if not component.transactions:
        ctk.CTkLabel(scroll_frame, text="No transactions yet.", text_color="gray").pack()
    else:
        for tx in component.transactions:
            # 1. Determine styling based on type
            if tx.type == TransactionType.INCOME:
                color = "#72bd39"      # Green
                icon_name = "income.png"
                prefix = "+"
            else:
                color = "#ff5555"      # Red
                icon_name = "expense.png"
                prefix = "-"

            # 2. Load the Icon
            try:
                icon_img = Image.open(f"icons/{icon_name}")
                ctk_icon = ctk.CTkImage(light_image=icon_img, dark_image=icon_img, size=(30, 30))
            except Exception:
                ctk_icon = None # Fallback if file is missing

            # 3. Create Row Frame
            tx_row = ctk.CTkFrame(scroll_frame, height=60, fg_color="#262626")
            tx_row.pack(fill="x", padx=20, pady=2)
            tx_row.pack_propagate(False)

            # --- LEFT SIDE: Date ---
            date_label = ctk.CTkLabel(tx_row, text=tx.date.strftime('%d.%m.%Y'), 
                                    font=("Courier New", 12), text_color="gray")
            date_label.pack(side="left", padx=10)

            # --- LEFT SIDE: Amount ---
            amt_label = ctk.CTkLabel(tx_row, text=f"{prefix}{tx.amount}€", 
                                    text_color=color, font=("Courier New", 14, "bold"))
            amt_label.pack(side="left", padx=5)

            
            # --- RIGHT SIDE: Icon (Arrow) ---
            if ctk_icon:
                icon_label = ctk.CTkLabel(tx_row, image=ctk_icon, text="")
                icon_label.pack(side="right", padx=(0, 10))
                
            # --- RIGHT SIDE: Note  ---
            note_label = ctk.CTkLabel(tx_row, text=tx.note, font=("Courier New", 14))
            note_label.pack(side="right", padx=(0, 30))
    
            
    

def refresh_list():
    for widget in scroll_frame.winfo_children():
        widget.destroy()
    for comp in financial_components:
        render_component(scroll_frame, comp)

def render_component(parent, component, height=80):
    # Main frame for the component - added cursor for UI feedback
    frame = ctk.CTkFrame(parent, height=height, fg_color="#1f1f1f", cursor="hand2")
    frame.pack(fill="x", pady=5, padx=5)


    def apply_bindings(widget):
        widget.bind("<Button-1>", lambda e: show_details(component))
        widget.bind("<Button-3>", lambda e: show_context_menu(e, component))
        for child in widget.winfo_children():
            apply_bindings(child)

    left_frame = ctk.CTkFrame(frame, fg_color="transparent")
    left_frame.pack(side="left", padx=10, pady=10, fill="x", expand=True)
    left_frame.bind("<Button-1>", lambda e: show_details(component))

    # Image handling using ctk.CTkImage
    if hasattr(component, "image_path") and component.image_path:
        try:
            img_data = Image.open(component.image_path)
            ctk_img = ctk.CTkImage(light_image=img_data, dark_image=img_data, size=(60, 60))
            img_label = ctk.CTkLabel(left_frame, image=ctk_img, text="")
            img_label.pack(side="left", padx=5)
            img_label.bind("<Button-1>", lambda e: show_details(component))
        except:
            pass # Handle missing file

    # Text
    text_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
    text_frame.pack(side="left", padx=10, fill="x", expand=True)
    text_frame.bind("<Button-1>", lambda e: show_details(component))

    name_label = ctk.CTkLabel(text_frame, text=component.name, font=("Courier New", 16, "bold"))
    name_label.pack(anchor="w")
    name_label.bind("<Button-1>", lambda e: show_details(component))

    apply_bindings(frame)

# Initial Render
refresh_list()

root.mainloop()
