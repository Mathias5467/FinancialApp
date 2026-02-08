import customtkinter as ctk
from PIL import Image, ImageTk
import ctypes
from functional_components import *

# --- Setup CTk ---
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

# --- Dragging functions ---
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


icon_image = Image.open("icons/logo.png") 
icon_image = icon_image.resize((24, 24), Image.LANCZOS)
icon_photo = ImageTk.PhotoImage(icon_image)


title_bar = ctk.CTkFrame(root, height=50, fg_color="#1f1f1f")
title_bar.pack(fill="x")

icon_label = ctk.CTkLabel(title_bar, image=icon_photo, text="")
icon_label.pack(side="left", padx=5)

title_label = ctk.CTkLabel(title_bar, text="Cash Flow", text_color="#72bd39", font=("Courier New", 16, "bold"), fg_color=None)
title_label.pack(side="left")


close_button = ctk.CTkButton(title_bar, text="✕", width=30, font=("Courier New", 16, "normal"),
                            command=root.destroy, fg_color="#1f1f1f", hover_color="#2d2d2d", text_color="#72bd39")
close_button.pack(side="right", padx=5, pady=5)

max_button = ctk.CTkButton(title_bar, text="☐", width=30, font=("Courier New", 16, "bold"),
                        command=maximize_restore_window, fg_color="#1f1f1f", hover_color="#2d2d2d", text_color="#72bd39")
max_button.pack(side="right", pady=5)

min_button = ctk.CTkButton(title_bar, text="─", width=30, font=("Courier New", 16, "bold"),
                        command=minimize_window, fg_color="#1f1f1f", hover_color="#2d2d2d", text_color="#72bd39")
min_button.pack(side="right", padx=5, pady=5)


# --- Bind dragging ---
title_bar.bind("<Button-1>", start_move)
title_bar.bind("<B1-Motion>", do_move)
title_label.bind("<Button-1>", start_move)
title_label.bind("<B1-Motion>", do_move)



financial_components = [
    Savings("Hypotéka", 25000, "icons/house.png", 10660),
    Savings("Svadba", 6000, "icons/wedding.png", 1200),
    Savings("Prsteň", 900, "icons/ring.png", 899),
    Budget("Spotreba", "icons/money.png", 457),
    Budget("Dlžia mi", "icons/money.png", 149.97),
    Savings("Hypotéka", 25000, "icons/house.png", 10660),
    Savings("Svadba", 6000, "icons/wedding.png", 1200),
    Savings("Prsteň", 900, "icons/ring.png", 899),
    Budget("Spotreba", "icons/money.png", 457),
    Budget("Dlžia mi", "icons/money.png", 149.97),
    Savings("Hypotéka", 25000, "icons/house.png", 10660),
    Savings("Svadba", 6000, "icons/wedding.png", 1200),
    Savings("Prsteň", 900, "icons/ring.png", 899),
    Budget("Spotreba", "icons/money.png", 457),
    Budget("Dlžia mi", "icons/money.png", 149.97),
    
]


# --- Main content frame ---
scroll_frame = ctk.CTkScrollableFrame(root, width=580, height=350)
scroll_frame.pack(fill="both", expand=True)

# --- Function to render a single component ---
def render_component(parent, component, height=80):
    # Main frame for the component
    frame = ctk.CTkFrame(parent, height=height, fg_color="#1f1f1f")
    frame.pack(fill="x", pady=5, padx=5)

    # --- Left side: image + name/details ---
    left_frame = ctk.CTkFrame(frame, fg_color="transparent")
    left_frame.pack(side="left", padx=10, pady=10, fill="x", expand=True)

    # Image or placeholder
    if hasattr(component, "image_path") and component.image_path:
        try:
            img = Image.open(component.image_path).resize((60, 60), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            img_label = ctk.CTkLabel(left_frame, image=photo, text="")
            img_label.image = photo
            img_label.pack(side="left", padx=5)
        except Exception:
            placeholder = ctk.CTkLabel(left_frame, text="🗂️", width=60, height=60,
                                       fg_color="#2d2d2d", corner_radius=10)
            placeholder.pack(side="left", padx=5)
    else:
        placeholder = ctk.CTkLabel(left_frame, text="🗂️", width=60, height=60,
                                   fg_color="#2d2d2d", corner_radius=10)
        placeholder.pack(side="left", padx=5)

    # Text: name + details
    text_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
    text_frame.pack(side="left", padx=10, fill="x", expand=True)

    name_label = ctk.CTkLabel(text_frame, text=component.name, 
                              font=("Courier New", 16, "bold"))
    name_label.pack(anchor="w")

    if isinstance(component, Savings):
        details = f"${component.current_amount} / ${component.target_amount}"
    elif isinstance(component, Budget):
        details = f"Current: ${component.current_amount}"
    else:
        details = f"${component.current_amount}"

    details_label = ctk.CTkLabel(text_frame, text=details, font=("Courier New", 14))
    details_label.pack(anchor="w")

    # --- Right side: ring for savings ---
    if isinstance(component, Savings):
        right_frame = ctk.CTkFrame(frame, fg_color="transparent", width=70)
        right_frame.pack(side="right", padx=10)

        size = 70
        size_text = 18
        thickness = 4
        canvas = ctk.CTkCanvas(right_frame, width=size, height=size,
                               bg=frame.cget("fg_color"), highlightthickness=0)
        canvas.pack()
        # background circle
        canvas.create_oval(thickness/2, thickness/2, size-thickness/2, size-thickness/2,
                           outline="#2d2d2d", width=thickness)
        # progress arc
        canvas.create_arc(thickness/2, thickness/2, size-thickness/2, size-thickness/2,
                          start=-90, extent=360*component.calculate_percent()/100,
                          outline="#72bd39", width=thickness, style="arc")
        # Percentage text inside ring
        canvas.create_text(size/2, size/2, text=f"{component.calculate_percent():.0f}%", 
                           fill="#72bd39", font=("Courier New", size_text, "bold"))




# --- Render all financial components ---
for comp in financial_components:
    render_component(scroll_frame, comp)



root.mainloop()
