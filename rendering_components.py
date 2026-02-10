import customtkinter as ctk
from PIL import Image, ImageTk
from functional_components import *


class Bar:
    def __init__(self, root, maximize_window, minimize_window, start_move, do_move, title="Cash Flow", icon_path="icons/logo.png"):
        self.root = root

        # OPRAVA: Použitie ctk.CTkImage namiesto ImageTk.PhotoImage
        icon_img = Image.open(icon_path)
        self.icon_photo = ctk.CTkImage(light_image=icon_img, dark_image=icon_img, size=(24, 24))

        self.title_bar = ctk.CTkFrame(root, height=50, fg_color="#1f1f1f")
        self.title_bar.grid(row=0, column=0, sticky="ew") # Použijeme grid

        self.icon_label = ctk.CTkLabel(self.title_bar, image=self.icon_photo, text="")
        self.icon_label.pack(side="left", padx=5)

        title_label = ctk.CTkLabel(self.title_bar, text=title, text_color="#72bd39", font=("Courier New", 16, "bold"))
        title_label.pack(side="left")

        # Tlačidlá
        self.close_button = ctk.CTkButton(self.title_bar, text="✕", width=30, command=root.destroy, fg_color="#1f1f1f", hover_color="#2d2d2d", text_color="#72bd39")
        self.close_button.pack(side="right", padx=5, pady=5)

        self.max_button = ctk.CTkButton(self.title_bar, text="☐", width=30, command=maximize_window, fg_color="#1f1f1f", hover_color="#2d2d2d", text_color="#72bd39")
        self.max_button.pack(side="right", pady=5)

        self.min_button = ctk.CTkButton(self.title_bar, text="─", width=30, command=minimize_window, fg_color="#1f1f1f", hover_color="#2d2d2d", text_color="#72bd39")
        self.min_button.pack(side="right", padx=5, pady=5)

        # Bindings
        self.title_bar.bind("<Button-1>", start_move)
        self.title_bar.bind("<B1-Motion>", do_move)
        title_label.bind("<Button-1>", start_move)
        title_label.bind("<B1-Motion>", do_move)

class ActionBar(ctk.CTkFrame):
    def __init__(self, parent, on_add_callback):
        super().__init__(parent, fg_color="transparent", height=50)
        self.on_add_callback = on_add_callback

        self.add_button = ctk.CTkButton(
            self, text="+", width=40, height=40,
            font=("Courier New", 24, "bold"),
            fg_color="#1f1f1f", text_color="#72bd39",
            hover_color="#2b2b2b", border_color="#72bd39",
            border_width=1, corner_radius=8,
            command=self.on_add_callback
        )
        self.add_button.pack(side="right", padx=30)

class ScrollableFrame(ctk.CTkScrollableFrame):
    def __init__(self, root, width, height):
        super().__init__(root, width=width, height=height)

class AddEntityFrame(ctk.CTkFrame):
    def __init__(self, parent, on_save_callback, on_cancel_callback):
        super().__init__(parent, fg_color="transparent")
        self.on_save_callback = on_save_callback
        self.on_cancel_callback = on_cancel_callback

        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(pady=20, padx=40, fill="x")

        # --- Tlačidlo Späť ---
        self.back_btn = ctk.CTkButton(
            self.container, text="◄ Back", width=80, 
            fg_color="transparent", border_color="#72bd39", border_width=1,
            command=self.on_cancel_callback
        )
        self.back_btn.pack(anchor="w", pady=(0, 20))

        # --- Nadpis ---
        self.header = ctk.CTkLabel(
            self.container, text="Nová kategória", 
            font=("Courier New", 24, "bold"), text_color="#72bd39"
        )
        self.header.pack(anchor="w")

        # --- Typ (Savings / Budget) ---
        ctk.CTkLabel(self.container, text="Typ:", font=("Courier New", 14)).pack(anchor="w", pady=(20, 5))
        self.type_var = ctk.StringVar(value="Savings")
        self.type_switch = ctk.CTkSegmentedButton(
            self.container, values=["Savings", "Budget"],
            variable=self.type_var, command=self._toggle_goal,
            selected_color="#72bd39"
        )
        self.type_switch.pack(fill="x", pady=(0, 10))

        # --- Názov ---
        ctk.CTkLabel(self.container, text="Názov:", font=("Courier New", 14)).pack(anchor="w", pady=(10, 5))
        self.name_entry = ctk.CTkEntry(self.container, placeholder_text="Napr. Dovolenka...", height=40)
        self.name_entry.pack(fill="x", pady=(0, 10))
        self.name_entry.bind("<Button-1>", lambda e: self.name_entry.focus_set())

        # --- Ikona (Len názov bez .png) ---
        ctk.CTkLabel(self.container, text="Názov ikony (napr. house, money...):", font=("Courier New", 14)).pack(anchor="w", pady=(10, 5))
        self.icon_entry = ctk.CTkEntry(self.container, placeholder_text="money", height=40)
        self.icon_entry.pack(fill="x", pady=(0, 10))

        # --- Cieľ (Goal) ---
        self.goal_label = ctk.CTkLabel(self.container, text="Cieľová suma (€):", font=("Courier New", 14))
        self.goal_label.pack(anchor="w", pady=(10, 5))
        self.goal_entry = ctk.CTkEntry(self.container, placeholder_text="5000", height=40)
        self.goal_entry.pack(fill="x", pady=(0, 10))

        # --- Tlačidlo Uložiť ---
        self.save_btn = ctk.CTkButton(
            self.container, text="Vytvoriť", 
            fg_color="#72bd39", hover_color="#5fa32f", height=50,
            command=self._handle_save
        )
        self.save_btn.pack(fill="x", pady=30)

    def _toggle_goal(self, choice):
        if choice == "Budget":
            self.goal_label.pack_forget()
            self.goal_entry.pack_forget()
        else:
            self.goal_label.pack(anchor="w", pady=(10, 5), before=self.save_btn)
            self.goal_entry.pack(fill="x", pady=(0, 10), before=self.save_btn)

    def _handle_save(self):
        name = self.name_entry.get().strip()
        icon = self.icon_entry.get().strip() or "money"
        e_type = self.type_var.get()
        
        if not name:
            self.name_entry.configure(border_color="red")
            return

        if e_type == "Savings":
            try:
                goal = float(self.goal_entry.get().replace(',', '.'))
                self.on_save_callback(e_type, name, goal, icon)
            except ValueError:
                self.goal_entry.configure(border_color="red")
        else:
            self.on_save_callback(e_type, name, 0, icon)

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
            raw_val = amt_entry.get().replace('€', '').replace(',', '.').strip()
            amount = float(raw_val)
            note = note_entry.get() if note_entry.get() else "No note"
            
            # Výpočet nového zostatku
            new_amount = self.component.current_amount + (amount if (trans_type==TransactionType.INCOME) else -amount)
            
            new_tx = Transaction(amount, trans_type, new_amount, datetime.now(), note=note)
            self.component.add_transaction(new_tx)
            
            # Uloženie dát
            from data_manager import save_data
            import __main__ # Prístup k financial_components z main.py
            save_data(__main__.financial_components) 

            # DÔLEŽITÉ: Uvoľniť grab pred zničením!
            self.grab_release()
            self.refresh_callback()
            self.destroy()
        except Exception as e:
            print(f"Chyba pri ukladaní: {e}")
            amt_entry.configure(border_color="#ff5555")

    # Pridaj aj do cancel tlačidla:
    def destroy_window(self):
        self.grab_release()
        self.destroy()


class AdaptableGraph(ctk.CTkCanvas):
    def __init__(self, master, data, color, **kwargs):
        kwargs.setdefault("height", 300)
        kwargs.setdefault("bg", "#1a1a1a")
        kwargs.setdefault("highlightthickness", 0)
        super().__init__(master, **kwargs)
        self.data = data
        self.color = color
        self.bind("<Configure>", lambda e: self.draw())

    def draw(self):
        self.delete("all")
        width = self.winfo_width()
        height = self.winfo_height()

        if width <= 1:
            self.after(100, self.draw)
            return

        if not self.data:
            self.create_text(width/2, height/2, text="Žiadne dáta", fill="gray", font=("Courier New", 12))
            return

        pad_l, pad_r, pad_t, pad_b = 60, 25, 25, 25
        
        max_v = max(self.data)
        min_v = min(self.data)
        v_range = (max_v - min_v) if max_v != min_v else (max_v if max_v != 0 else 1)

        # --- DYNAMICKÁ MRIEŽKA PODĽA POČTU PRVKOV ---
        # Počet krokov (riadkov) je rovný počtu prvkov v zozname
        steps = len(self.data)
        # Divisor (deliteľ) musí byť aspoň 1, aby sme sa vyhli deleniu nulou
        divisor = (steps - 1) if steps > 1 else 1

        for i in range(steps):
            # Výpočet Y pozície pre každý riadok mriežky
            y = pad_t + (i * (height - pad_t - pad_b) / divisor)
            
            # Kreslenie mriežky
            self.create_line(pad_l, y, width - pad_r, y, fill="#2d2d2d", dash=(2, 2))
            
            # Výpočet hodnoty pre popisok na Y osi
            # (Rovnomerne rozložené hodnoty od Max po Min)
            val = max_v - (i * v_range / divisor)
            self.create_text(pad_l - 10, y, text=f"{val:.0f}€", 
                             fill="gray", anchor="e", font=("Courier New", 10))

        # --- KRESLENIE DÁT (Body a Čiara) ---
        points = []
        for i, val in enumerate(self.data):
            # X pozícia (rovnomerne rozdelená)
            x = pad_l + (i * (width - pad_l - pad_r) / divisor)
            
            # Y pozícia (normalizovaná hodnota)
            norm = (val - min_v) / v_range
            y = (height - pad_b) - (norm * (height - pad_t - pad_b))
            points.append((x, y))

        # Kreslenie čiary (priama spojnica bez smooth)
        if len(points) > 1:
            self.create_line(points, fill=self.color, width=3)
        
        # Kreslenie bodov
        for x, y in points:
            self.create_oval(x-4, y-4, x+4, y+4, fill=self.color, outline="#1a1a1a", width=1)

class CombinedGraph(ctk.CTkCanvas):
    def __init__(self, master, transactions, **kwargs):
        kwargs.setdefault("height", 400)
        kwargs.setdefault("bg", "#1a1a1a")
        kwargs.setdefault("highlightthickness", 0)
        super().__init__(master, **kwargs)
        self.transactions = transactions
        self.bind("<Configure>", lambda e: self.draw())

    def draw(self):
        self.delete("all")
        width = self.winfo_width()
        height = self.winfo_height()

        if width <= 1:
            self.after(100, self.draw)
            return

        if not self.transactions:
            self.create_text(width/2, height/2, text="Žiadne transakcie", fill="gray")
            return

        pad_l, pad_r, pad_t, pad_b = 60, 25, 25, 25
        amounts = [t.current_amount for t in self.transactions]
        max_v, min_v = max(amounts), min(amounts)
        v_range = (max_v - min_v) if max_v != min_v else (max_v if max_v != 0 else 1)

        # Mriežka
        for i in range(5):
            y = pad_t + (i * (height - pad_t - pad_b) / 4)
            self.create_line(pad_l, y, width - pad_r, y, fill="#2d2d2d", dash=(2, 2))
            val = max_v - (i * v_range / 4)
            self.create_text(pad_l - 10, y, text=f"{val:.0f}€", fill="gray", anchor="e", font=("Courier New", 10))

        # Body
        points = []
        for i, tx in enumerate(self.transactions):
            x = pad_l + (i * (width - pad_l - pad_r) / (max(1, len(self.transactions)-1)))
            norm = (tx.current_amount - min_v) / v_range
            y = (height - pad_b) - (norm * (height - pad_t - pad_b))
            points.append((x, y, tx.type))

        if len(points) > 1:
            coords = [(p[0], p[1]) for p in points]
            self.create_line(coords, fill="#3d3d3d", width=1, dash=(4, 4))

        for x, y, t_type in points:
            color = "#72bd39" if t_type == TransactionType.INCOME else "#ff5555"
            self.create_oval(x-4, y-4, x+4, y+4, fill=color, outline="white")
        # Prechádzame body od druhého (index 1) a spájame ho s predchádzajúcim
        if len(points) > 1:
            for i in range(1, len(points)):
                prev_x, prev_y, _ = points[i-1]
                curr_x, curr_y, curr_type = points[i]
                
                # Farba čiary podľa typu transakcie, ktorá tento bod vytvorila
                line_color = "#72bd39" if curr_type == TransactionType.INCOME else "#ff5555"
                
                # Nakreslíme spojnicu medzi bodmi
                self.create_line(prev_x, prev_y, curr_x, curr_y, 
                                 fill=line_color, width=3) # Width 3 pre lepšiu viditeľnosť

        # 4. Kreslenie bodov navrch (aby prekrývali čiary)
        for x, y, t_type in points:
            color = "#72bd39" if t_type == TransactionType.INCOME else "#ff5555"
            # Väčší bod s bielym obrysom
            self.create_oval(x-5, y-5, x+5, y+5, fill=color, outline="white", width=1)