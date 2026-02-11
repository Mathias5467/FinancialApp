import customtkinter as ctk
from PIL import Image
import ctypes
import tkinter as tk

from functional_components import *
from rendering_components import *
from data_manager import save_data, load_data


# --- Color themes ---
color_themes = [{"bg1": "#B4CDED", "bg2": "#344966", "font": "#0D1821"},
                {"bg1": "#343E3D", "bg2": "#607466", "font": "#AEDCC0"},
                {"bg1": "#D6D1B1", "bg2": "#F0B67F", "font": "#FE5F55"},
                {"bg1": "#5A7D7C", "bg2": "#232C33", "font": "#DADFF7"},
                {"bg1": "#DCDCDD", "bg2": "#C5C3C6", "font": "#46494C"}]

color_bg1 = color_themes[1]["bg1"]
color_bg2 = color_themes[1]["bg2"]
color_font = color_themes[1]["font"]


# --- Setup CTk ---
ctk.set_appearance_mode("dark")
root = ctk.CTk() 
root.configure(fg_color=color_bg1)
root.geometry("1000x600")

# --- Setting up grid (first column -> 0, this column will enlarge) ---
root.columnconfigure(0, weight=1)
root.rowconfigure(2, weight=1)

# --- Window Decoration (Windows only) ---
root.iconbitmap("icons/logo.ico")
root.overrideredirect(True)
hwnd = ctypes.windll.user32.GetParent(root.winfo_id())
ctypes.windll.user32.SetWindowLongW(hwnd, -16, 0x10000000 | 0x40000000)
ctypes.windll.user32.SetWindowLongW(hwnd, -20, ctypes.windll.user32.GetWindowLongW(hwnd, -20) & ~0x80)
ctypes.windll.user32.SetWindowLongW(hwnd, -20, ctypes.windll.user32.GetWindowLongW(hwnd, -20) | 0x00040000)
ctypes.windll.user32.ShowWindow(hwnd, 5)

# --- Window Dragging Logic ---
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

def maximize_restore_window():
    if root.state() == "normal":
        root.state("zoomed")
    else:
        root.state("normal")


# --- Inicial loading of data ---
financial_components = load_data()


# --- Logic of creating new entity saving it into json ---
def create_new_financial_entity(e_type, name, goal, icon):
    if e_type == "Savings":
        new_obj = Savings(name, goal, icon, 0)
    else:
        new_obj = Budget(name, icon, 0)
    
    financial_components.append(new_obj)
    refresh_list()


# --- View of  ---
def add_financial_entity_view():
    action_bar.grid_remove()
    for widget in scroll_frame.winfo_children():
        widget.destroy()
    
    add_form = AddEntityFrame(scroll_frame, create_new_financial_entity, refresh_list)
    add_form.pack(fill="both", expand=True)
    
    # Vynútenie fokusu na okno
    root.after(100, lambda: add_form.name_entry.focus_set())
    root.after(100, lambda: root.focus_force())


# TODO: Make this create frame where you can choose color theme
def select_color_theme_view():
    pass

def refresh_list():
    
    action_bar.grid(row=1, column=0)
    
    for widget in scroll_frame.winfo_children():
        widget.destroy()
    else:
        for comp in financial_components:
            render_created_financial_entities(scroll_frame, comp)

def show_details(component):
    """Zobrazí detaily a skryje action bar."""
    action_bar.grid_remove()
    
    for widget in scroll_frame.winfo_children():
        widget.destroy()

    # Back Button
    back_btn = ctk.CTkButton(scroll_frame, text="◄ Back", height=30, width=30,
                             fg_color="transparent", hover_color=color_bg2,
                             border_color=color_bg2, border_width=2, font=("Courier New", 18, "normal"),
                             text_color=color_font,
                             command=refresh_list)
    back_btn.pack(anchor="w", padx=12, pady=4)

    # Main Detail Container
    detail_container = ctk.CTkFrame(scroll_frame, fg_color="transparent")
    detail_container.pack(fill="x", padx=10, pady=10)
    detail_container.columnconfigure(0, weight=1)
    detail_container.columnconfigure(1, weight=0)

    # Left side (Text)
    text_info_frame = ctk.CTkFrame(detail_container, fg_color="transparent")
    text_info_frame.grid(row=0, column=0, sticky="nsw", padx=10)
    def fmt(amount):
        return f"{amount:,.0f}".replace(",", " ")

    

    ctk.CTkLabel(text_info_frame, text=component.name, 
                 font=("Courier New", 50, "bold"), text_color=color_font).pack(anchor="w")

    amt_text = (
        f"{fmt(component.current_amount)}/{fmt(component.target_amount)}€"
        if isinstance(component, Savings)
        else f"{fmt(component.current_amount)}€"
    )
    ctk.CTkLabel(text_info_frame, text=amt_text, font=("Courier New", 18), text_color=color_font).pack(anchor="w", pady=(15, 40))

    # Right side (Ring)
    if isinstance(component, Savings):
        ring_frame = ctk.CTkFrame(detail_container, fg_color="transparent")
        ring_frame.grid(row=0, column=1, padx=20, sticky="ne")
        
        size, thickness = 120, 8
        percent = component.calculate_percent()
        canvas = ctk.CTkCanvas(ring_frame, width=size, height=size, bg=color_bg1, highlightthickness=0)
        canvas.pack()
        canvas.create_oval(thickness, thickness, size-thickness, size-thickness, outline=color_bg2, width=thickness)
        canvas.create_arc(thickness, thickness, size-thickness, size-thickness, start=90, extent=360 * (percent / 100), outline=color_font, width=thickness, style="arc")
        canvas.create_text(size/2, size/2, text=f"{percent:.0f}%", fill=color_font, font=("Courier New", 22, "bold"))

    # Transactions List
    ctk.CTkLabel(scroll_frame, text="Recent Transactions", font=("Courier New", 18, "bold"), text_color=color_font).pack(pady=(30, 10))
    if not component.transactions:
        ctk.CTkLabel(scroll_frame, text="No transactions yet.", text_color="gray").pack()
    else:
        for tx in component.transactions:
            color = "#57aa17" if tx.type == TransactionType.INCOME else "#993C3C"
            prefix = "+" if tx.type == TransactionType.INCOME else "-"
            
            tx_row = ctk.CTkFrame(scroll_frame, height=60, fg_color=color_bg2)
            tx_row.pack(fill="x", padx=20, pady=2)
            tx_row.pack_propagate(False)

            ctk.CTkLabel(tx_row, text=tx.date.strftime('%d.%m.%Y'), font=("Courier New", 15, "bold"), text_color=color_bg1).pack(side="left", padx=10)
            ctk.CTkLabel(tx_row, text=f"{prefix}{tx.amount:.2f}€", text_color=color, font=("Courier New", 17, "bold")).pack(side="left", padx=5)
            ctk.CTkLabel(tx_row, text=tx.note, font=("Courier New", 15), text_color=color_font).pack(side="right", padx=(0, 30))

    # Graphs
    graph_container = ctk.CTkFrame(scroll_frame, fg_color="transparent")
    graph_container.pack(fill="x", padx=30, pady=20)

    income_data = [t.amount for t in component.transactions if t.type == TransactionType.INCOME]
    income_data.insert(0, 0)
    expense_data = [t.amount for t in component.transactions if t.type == TransactionType.EXPENSE]
    expense_data.insert(0, 0)


    ctk.CTkLabel(graph_container, text="Príjmy", font=("Courier New", 18, "bold"), text_color="#72bd39").pack(anchor="w")
    AdaptableGraph(graph_container, data=income_data, color="#72bd39").pack(fill="x", pady=(5, 25))

    ctk.CTkLabel(graph_container, text="Výdavky", font=("Courier New", 18, "bold"), text_color="#ff5555").pack(anchor="w")
    AdaptableGraph(graph_container, data=expense_data, color="#ff5555").pack(fill="x", pady=(5, 25))

    ctk.CTkLabel(graph_container, text="História transakcií", font=("Courier New", 18, "bold"), text_color="white").pack(anchor="w")
    CombinedGraph(graph_container, transactions=component.transactions).pack(fill="x", pady=(5, 25))

# --- Main Components Creation ---

# Riadok 0: Title bar
title_bar_comp = Bar(root, color_bg2, color_font, maximize_restore_window, minimize_window, start_move, do_move, "Cash Flow", "icons/logo.png")
# Poznámka: Predpokladám, že Bar trieda vo vnútri používa .grid(row=0) alebo ju tam umiestniš manuálne.

# Riadok 1: Action bar
action_bar = ActionBar(root, add_financial_entity_view, select_color_theme_view, color_bg1, color_bg2, color_font)
action_bar.grid(row=1, column=0, sticky="ew", pady=(10, 0), padx=(18, 0))

# Riadok 2: Scrollable frame
scroll_frame = ScrollableFrame(root, 580, 350, color_bg1)
scroll_frame.grid(row=2, column=0, sticky="nsew", padx=(0, 0), pady=0)

# --- Component Rendering ---

def render_created_financial_entities(parent, component, height=80):
    frame = ctk.CTkFrame(parent, height=height, fg_color=color_bg2, cursor="hand2")
    frame.pack(fill="x", pady=5, padx=10)

    def apply_bindings(widget):
        widget.bind("<Button-1>", lambda e: show_details(component))
        widget.bind("<Button-3>", lambda e: show_context_menu(e, component))
        for child in widget.winfo_children():
            apply_bindings(child)

    left_frame = ctk.CTkFrame(frame, fg_color="transparent")
    left_frame.pack(side="left", padx=10, pady=10, fill="x", expand=True)

    # OPRAVA VAROVANIA: Použitie ctk.CTkImage namiesto ImageTk
    if hasattr(component, "image_path") and component.image_path:
        try:
            img_data = Image.open(component.image_path)
            ctk_img = ctk.CTkImage(light_image=img_data, dark_image=img_data, size=(60, 60))
            img_label = ctk.CTkLabel(left_frame, image=ctk_img, text="")
            img_label.pack(side="left", padx=5)
        except:
            pass

    text_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
    text_frame.pack(side="left", padx=10, fill="x", expand=True)

    name_label = ctk.CTkLabel(text_frame, text=component.name, font=("Courier New", 16, "bold"), text_color=color_font)
    name_label.pack(anchor="w")

    apply_bindings(frame)

def show_context_menu(event, component):
    TransactionWindow(root, component, refresh_list, color_bg1, color_bg2, color_font)

# Initial Run
refresh_list()
root.mainloop()