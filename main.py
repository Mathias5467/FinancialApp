import customtkinter as ctk
from PIL import Image
import ctypes
import tkinter as tk
import os

from functional_components import *
from rendering_components import *
from data_manager import save_data, load_data
import color_themes as ct # Use 'import' so we access the module's state

actual_colors = {}

def change_theme(number_of_theme):
    global actual_colors
    ct.set_color_index(number_of_theme)

    actual_colors = ct.color_themes[number_of_theme]

change_theme(1)

# --- Setup CTk ---
ctk.set_appearance_mode("dark")
root = ctk.CTk() 
root.configure(fg_color=actual_colors["bg1"])
root.geometry("1000x600")

# --- Setting up grid (first column -> 0, this column will enlarge) ---
root.columnconfigure(0, weight=1)
root.rowconfigure(2, weight=1)

icon_path = resource_path("icons/logo.ico")
if os.path.exists(icon_path):
    root.iconbitmap(icon_path)

# --- Window Decoration (Windows only) ---
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
    scroll_frame.grid_remove()
    
    def handle_back():
        add_form.destroy()
        refresh_list() 
    
    add_form = AddEntityFrame(root, create_new_financial_entity, handle_back, actual_colors)
    add_form.grid(row=1, column=0, rowspan=2, sticky="nsew", padx=(8, 10), pady=6)
    
    # Vynútenie fokusu na okno
    root.after(100, lambda: add_form.name_entry.focus_set())
    root.after(100, lambda: root.focus_force())


# TODO: Make this create frame where you can choose color theme
def select_color_theme_view():
    pass


def refresh_list():
    
    action_bar.grid(row=1, column=0, sticky="ew", pady=(10, 0), padx=(18, 0))
    scroll_frame.grid(row=2, column=0, sticky="nsew")
    for widget in scroll_frame.winfo_children():
        widget.destroy()
    
    for comp in financial_components:
        render_created_financial_entities(scroll_frame, comp)

def show_details(component):
    """Zobrazí detaily a skryje action bar."""
    action_bar.grid_remove()
    
    for widget in scroll_frame.winfo_children():
        widget.destroy()

    # Back Button
    back_btn = ctk.CTkButton(scroll_frame, text="◄ Back", height=30, width=30,
                             fg_color="transparent", hover_color=actual_colors["bg2"],
                             border_color=actual_colors["bg2"], border_width=2, font=("Courier New", 18, "normal"),
                             text_color=actual_colors["font"],
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
                 font=("Courier New", 50, "bold"), text_color=actual_colors["font"]).pack(anchor="w")

    amt_text = (
        f"{fmt(component.current_amount)}/{fmt(component.target_amount)}€"
        if isinstance(component, Savings)
        else f"{fmt(component.current_amount)}€"
    )
    ctk.CTkLabel(text_info_frame, text=amt_text, font=("Courier New", 18), text_color=actual_colors["font"]).pack(anchor="w", pady=(15, 40))

    # Right side (Ring)
    if isinstance(component, Savings):
        ring_frame = ctk.CTkFrame(detail_container, fg_color="transparent")
        ring_frame.grid(row=0, column=1, padx=20, sticky="ne")
        
        size, thickness = 120, 8
        percent = component.calculate_percent()
        canvas = ctk.CTkCanvas(ring_frame, width=size, height=size, bg=actual_colors["bg1"], highlightthickness=0)
        canvas.pack()
        canvas.create_oval(thickness, thickness, size-thickness, size-thickness, outline=actual_colors["bg2"], width=thickness)
        canvas.create_arc(thickness, thickness, size-thickness, size-thickness, start=90, extent=360 * (percent / 100), outline=actual_colors["font"], width=thickness, style="arc")
        canvas.create_text(size/2, size/2, text=f"{percent:.0f}%", fill=actual_colors["font"], font=("Courier New", 22, "bold"))

    # Transactions List
    ctk.CTkLabel(scroll_frame, text="Recent Transactions", font=("Courier New", 18, "bold"), text_color=actual_colors["font"]).pack(pady=(30, 10))
    if not component.transactions:
        ctk.CTkLabel(scroll_frame, text="No transactions yet.", text_color="gray").pack()
    else:
        
        for tx in component.transactions[::-1]:
            color = actual_colors["green"] if tx.type == TransactionType.INCOME else actual_colors["red"]
            prefix = "+" if tx.type == TransactionType.INCOME else "-"
            
            tx_row = ctk.CTkFrame(scroll_frame, height=60, fg_color=actual_colors["bg2"])
            tx_row.pack(fill="x", padx=20, pady=2)
            tx_row.pack_propagate(False)

            ctk.CTkLabel(tx_row, text=tx.date.strftime('%d.%m.%Y'), font=("Courier New", 15, "bold"), text_color=actual_colors["font"]).pack(side="left", padx=10)
            ctk.CTkLabel(tx_row, text=f"{prefix}{tx.amount:.2f}€", text_color=color, font=("Courier New", 17, "bold")).pack(side="left", padx=5)
            ctk.CTkLabel(tx_row, text=tx.note, font=("Courier New", 15, "bold"), text_color=actual_colors["font"]).pack(side="right", padx=(0, 30))

    # Graphs
    graph_container = ctk.CTkFrame(scroll_frame, fg_color="transparent")
    graph_container.pack(fill="x", padx=30, pady=20)

    # Filter full transaction objects instead of just amounts
    income_transactions = [t for t in component.transactions if t.type == TransactionType.INCOME]
    expense_transactions = [t for t in component.transactions if t.type == TransactionType.EXPENSE]
    
    # Príjmy Graph
    ctk.CTkLabel(graph_container, text="Príjmy", font=("Courier New", 18, "bold"), text_color=actual_colors["green"]).pack(anchor="w")
    AdaptableGraph(graph_container, transactions=income_transactions, color=actual_colors["green"], actual_colors=actual_colors).pack(fill="x", pady=(5, 25))

    # Výdavky Graph
    ctk.CTkLabel(graph_container, text="Výdavky", font=("Courier New", 18, "bold"), text_color=actual_colors["red"]).pack(anchor="w")
    AdaptableGraph(graph_container, transactions=expense_transactions, color=actual_colors["red"], actual_colors=actual_colors).pack(fill="x", pady=(5, 25))

    # Celková História
    ctk.CTkLabel(graph_container, text="História transakcií", font=("Courier New", 18, "bold"), text_color=actual_colors["font"]).pack(anchor="w")
    CombinedGraph(graph_container, transactions=component.transactions, actual_colors=actual_colors).pack(fill="x", pady=(5, 25))

# --- Main Components Creation ---

# --- Save data and exit ---
def save_exit():
    save_data(financial_components)
    root.destroy()


# Riadok 0: Title bar
title_bar_comp = Bar(root,actual_colors, maximize_restore_window, minimize_window, start_move, do_move, save_exit, "Cash Flow", resource_path("icons/logo.png"))
# Poznámka: Predpokladám, že Bar trieda vo vnútri používa .grid(row=0) alebo ju tam umiestniš manuálne.

# Riadok 1: Action bar
action_bar = ActionBar(root, add_financial_entity_view, select_color_theme_view, actual_colors)
action_bar.grid(row=1, column=0, sticky="ew", pady=(10, 0), padx=(18, 0))

# Riadok 2: Scrollable frame
scroll_frame = ScrollableFrame(root, 580, 350, actual_colors["bg1"])
scroll_frame.grid(row=2, column=0, sticky="nsew", padx=(0, 0), pady=0)

# --- Component Rendering ---

def render_created_financial_entities(parent, component, height=80):
    frame = ctk.CTkFrame(parent, height=height, fg_color=actual_colors["bg2"], cursor="hand2")
    frame.pack(fill="x", pady=5, padx=10)

    def apply_bindings(widget):
        widget.bind("<Button-1>", lambda e: show_details(component))
        widget.bind("<Button-3>", lambda e: show_context_menu(e, component))
        for child in widget.winfo_children():
            apply_bindings(child)

    left_frame = ctk.CTkFrame(frame, fg_color="transparent")
    left_frame.pack(side="left", padx=10, pady=10, fill="x", expand=True)

    
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

    name_label = ctk.CTkLabel(text_frame, text=component.name, font=("Courier New", 16, "bold"), text_color=actual_colors["font"])
    name_label.pack(anchor="w")

    apply_bindings(frame)

def show_context_menu(event, component):
    TransactionWindow(root, component, refresh_list, actual_colors)

# Initial Run
refresh_list()
root.mainloop()