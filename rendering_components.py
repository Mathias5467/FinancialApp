import customtkinter as ctk
from PIL import Image, ImageTk
from functional_components import *


class Bar:
    def __init__(self, root, maximize_window, minimize_window, start_move, do_move, title="Cash Flow", icon_path="icons/logo.png"):
        self.root = root

        # icon
        icon_image = Image.open("icons/logo.png") 
        icon_image = icon_image.resize((24, 24), Image.LANCZOS)
        self.icon_photo = ImageTk.PhotoImage(icon_image)

        # title bar frame
        self.title_bar = ctk.CTkFrame(root, height=50, fg_color="#1f1f1f")
        self.title_bar.pack(fill="x")

        # icon label
        self.icon_label = ctk.CTkLabel(self.title_bar, image=self.icon_photo, text="")
        self.icon_label.pack(side="left", padx=5)

        # title label
        title_label = ctk.CTkLabel(self.title_bar, text="Cash Flow", text_color="#72bd39", font=("Courier New", 16, "bold"), fg_color=None)
        title_label.pack(side="left")


        # close button
        self.close_button = ctk.CTkButton(self.title_bar, text="✕", width=30, font=("Courier New", 16, "normal"),
                                    command=root.destroy, fg_color="#1f1f1f", hover_color="#2d2d2d", text_color="#72bd39")
        self.close_button.pack(side="right", padx=5, pady=5)

        # maximize button
        self.max_button = ctk.CTkButton(self.title_bar, text="☐", width=30, font=("Courier New", 16, "bold"),
                                command=maximize_window, fg_color="#1f1f1f", hover_color="#2d2d2d", text_color="#72bd39")
        self.max_button.pack(side="right", pady=5)

        # minimize button
        self.min_button = ctk.CTkButton(self.title_bar, text="─", width=30, font=("Courier New", 16, "bold"),
                                command=minimize_window, fg_color="#1f1f1f", hover_color="#2d2d2d", text_color="#72bd39")
        self.min_button.pack(side="right", padx=5, pady=5)


        # bind dragging
        self.title_bar.bind("<Button-1>", start_move)
        self.title_bar.bind("<B1-Motion>", do_move)
        title_label.bind("<Button-1>", start_move)
        title_label.bind("<B1-Motion>", do_move)


class ScrollableFrame(ctk.CTkScrollableFrame):
    def __init__(self, root, width, height):
        super().__init__(root, width=width, height=height)
        self.pack(fill="both", expand=True)

class TransactionWindow(ctk.CTkToplevel):
    def __init__(self, parent, component, refresh_callback):
        super().__init__(parent)
        
        # 1. Window Setup
        self.width = 350
        self.height = 320 # Slightly reduced height since title bar is gone
        self.overrideredirect(True) 
        self.attributes("-topmost", True) 
        
        # Window background matches the border color
        self.configure(fg_color="#72bd39") 
        
        self.component = component
        self.refresh_callback = refresh_callback

        # 2. THE MAIN CONTAINER
        self.main_border_frame = ctk.CTkFrame(
            self, 
            corner_radius=0, 
            border_width=2, 
            border_color="#345819", 
            fg_color="#1f1f1f",
        )
        self.main_border_frame.pack(fill="both", expand=True)

        # 3. Tab View (Directly inside main frame)
        self.tabs = ctk.CTkTabview(self.main_border_frame, 
                                   segmented_button_selected_color="#72bd39",
                                   segmented_button_unselected_hover_color="#2d2d2d")
        self.tabs.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.tab_income = self.tabs.add("Income")
        self.tab_expense = self.tabs.add("Expense")

        # Setup forms
        self.setup_form(self.tab_income, TransactionType.INCOME)
        self.setup_form(self.tab_expense, TransactionType.EXPENSE)

        # 4. Centering and Focus
        self.center_to_root(parent)
        self.grab_set() 

    def center_to_root(self, root):
        root.update_idletasks()
        root_x = root.winfo_x()
        root_y = root.winfo_y()
        root_width = root.winfo_width()
        root_height = root.winfo_height()

        spawn_x = (root_x + (root_width // 2) - (self.width // 2)) - 20
        spawn_y = (root_y + (root_height // 2) - (self.height // 2)) - 30
        self.geometry(f"{self.width}x{self.height}+{spawn_x}+{spawn_y}")

    def setup_form(self, tab, trans_type):
        # Amount
        ctk.CTkLabel(tab, text="Amount:", font=("Courier New", 13)).pack(pady=(15, 0))
        amt_entry = ctk.CTkEntry(tab, placeholder_text="0.00€", width=220)
        amt_entry.pack(pady=5)

        # Note
        ctk.CTkLabel(tab, text="Note:", font=("Courier New", 13)).pack(pady=(10, 0))
        note_entry = ctk.CTkEntry(tab, placeholder_text="Description...", width=220)
        note_entry.pack(pady=5)

        # --- Button Container (Side-by-Side) ---
        button_frame = ctk.CTkFrame(tab, fg_color="transparent")
        button_frame.pack(pady=25)


            # Save Button (Green)
        submit_btn = ctk.CTkButton(button_frame, text="Save",
                                width=100,
                                fg_color="#72bd39",
                                text_color="white",
                                hover_color="#5fa32f", # Slightly darker green for hover effect
                                command=lambda: self.save_transaction(amt_entry, note_entry, trans_type))
        submit_btn.pack(side="left", padx=10)

        # Cancel Button (Red)
        cancel_btn = ctk.CTkButton(button_frame, text="Cancel",
                                width=100,
                                fg_color="#ff5555",
                                hover_color="#c94444", # Slightly darker red for hover effect
                                text_color="white",
                                command=self.destroy)
        cancel_btn.pack(side="left", padx=10)

        

    def save_transaction(self, amt_entry, note_entry, trans_type):
        try:
            # Clean input
            raw_val = amt_entry.get().replace('€', '').replace(',', '.').strip()
            amount = float(raw_val)
            note = note_entry.get() if note_entry.get() else "No note"
            
            new_tx = Transaction(amount, trans_type, note=note)
            self.component.add_transaction(new_tx)
            
            self.refresh_callback()
            self.destroy()
        except ValueError:
            amt_entry.configure(border_color="#ff5555")