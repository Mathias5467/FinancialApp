import customtkinter as ctk
from PIL import Image, ImageTk
from functional_components import *

class Bar:
    def __init__(self, root, actual_colors, maximize_window, minimize_window, start_move, do_move, save, title="Cash Flow", icon_path="icons/logo.png"):
        self.root = root

    
        icon_img = Image.open(resource_path(icon_path))
        self.icon_photo = ctk.CTkImage(light_image=icon_img, dark_image=icon_img, size=(24, 24))

        self.title_bar = ctk.CTkFrame(root, height=50, fg_color=actual_colors["bg2"], corner_radius=0)
        self.title_bar.grid(row=0, column=0, sticky="ew")

        self.icon_label = ctk.CTkLabel(self.title_bar, image=self.icon_photo, text="")
        self.icon_label.pack(side="left", padx=5)

        title_label = ctk.CTkLabel(self.title_bar, text=title, text_color=actual_colors["font"], font=("Courier New", 16, "bold"))
        title_label.pack(side="left")

        # Tlačidlá
        self.close_button = ctk.CTkButton(self.title_bar, text="✕", font=("Arial", 14, "bold"), width=30, command=save, fg_color=actual_colors["bg2"], hover_color=actual_colors["bg1"], text_color=actual_colors["font"])
        self.close_button.pack(side="right", padx=5, pady=5)

        self.max_button = ctk.CTkButton(self.title_bar, text="☐", font=("Arial", 14, "bold"), width=30, command=maximize_window, fg_color=actual_colors["bg2"], hover_color=actual_colors["bg1"], text_color=actual_colors["font"])
        self.max_button.pack(side="right", pady=5)

        self.min_button = ctk.CTkButton(self.title_bar, text="─", font=("Arial", 14, "bold"), width=30, command=minimize_window, fg_color=actual_colors["bg2"], hover_color=actual_colors["bg1"], text_color=actual_colors["font"])
        self.min_button.pack(side="right", padx=5, pady=5)



        # Bindings
        self.title_bar.bind("<Button-1>", start_move)
        self.title_bar.bind("<B1-Motion>", do_move)
        title_label.bind("<Button-1>", start_move)
        title_label.bind("<B1-Motion>", do_move)

class ActionBar(ctk.CTkFrame):
    def __init__(self, parent, on_add_callback, on_color_select_callback, actual_colors):
        super().__init__(parent, fg_color="transparent", height=50)
        self.on_add_callback = on_add_callback
        self.on_color_select_callback = on_color_select_callback
        self.add_button = ctk.CTkButton(
            self, text="Add new ►", height=30, width=30,
            font=("Courier New", 15, "normal"),
            fg_color=actual_colors["bg1"], text_color=actual_colors["font"],
            hover_color=actual_colors["bg2"], border_color=actual_colors["bg2"],
            border_width=2, corner_radius=8,
            command=self.on_add_callback
        )
        self.add_button.pack(side="left")

        self.color_theme_button = ctk.CTkButton(
            self, text="Select Theme", height=30, width=30,
            font=("Courier New", 15, "normal"),
            fg_color=actual_colors["bg1"], text_color=actual_colors["font"],
            hover_color=actual_colors["bg2"], border_color=actual_colors["bg2"],
            border_width=2, corner_radius=8,
            command=self.on_color_select_callback
        )
        self.color_theme_button.pack(side="left", padx=10)

class ScrollableFrame(ctk.CTkScrollableFrame):
    def __init__(self, root, width, height, color):
        super().__init__(root, width=width, height=height, fg_color=color)

class AddEntityFrame(ctk.CTkFrame):
    def __init__(self, parent, on_save_callback, on_cancel_callback, actual_colors):
        super().__init__(parent, fg_color="transparent")
        self.on_save_callback = on_save_callback
        self.on_cancel_callback = on_cancel_callback

        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(pady=4, padx=10, fill="x")

        # --- Tlačidlo Späť ---
        self.back_btn = ctk.CTkButton(
            self.container, text="◄ Back", height=30, width=30,
            fg_color="transparent", hover_color=actual_colors["bg2"],
            border_color=actual_colors["bg2"], border_width=2, font=("Courier New", 15, "normal"),
            text_color=actual_colors["font"],
            command=self.on_cancel_callback 
        )
        self.back_btn.pack(anchor="w", pady=(0, 20))


        # --- Typ (Savings / Budget) ---
        ctk.CTkLabel(self.container, text="Type:", font=("Courier New", 14, "bold"), text_color=actual_colors["font"]).pack(anchor="w", pady=(20, 5))
        self.type_var = ctk.StringVar(value="Savings")
        self.type_switch = ctk.CTkSegmentedButton(
            self.container, values=["Savings", "Budget"], font=("Courier New", 16, "bold"),
            variable=self.type_var, command=self._toggle_goal, height=40, fg_color=actual_colors["bg1"], unselected_hover_color= actual_colors["bg1"],
            selected_color=actual_colors["bg2"], selected_hover_color=actual_colors["bg2"], unselected_color= actual_colors["bg1"], text_color=actual_colors["font"]
        )
        self.type_switch.pack(fill="x", pady=(0, 10))

        # --- Názov ---
        ctk.CTkLabel(self.container, text="Name:", font=("Courier New", 14, "bold"), text_color=actual_colors["font"]).pack(anchor="w", pady=(10, 5))
        self.name_entry = ctk.CTkEntry(self.container, placeholder_text="Holidays...", height=40, fg_color=actual_colors["bg1"], text_color=actual_colors["font"])
        self.name_entry.pack(fill="x", pady=(0, 10))
        self.name_entry.bind("<Button-1>", lambda e: self.name_entry.focus_set())

        # --- Ikona (Len názov bez .png) ---
        ctk.CTkLabel(self.container, text="Icon name:", font=("Courier New", 14, "bold"), text_color=actual_colors["font"]).pack(anchor="w", pady=(10, 5))
        self.icon_entry = ctk.CTkEntry(self.container, placeholder_text="money", height=40, fg_color=actual_colors["bg1"], text_color=actual_colors["font"])
        self.icon_entry.pack(fill="x", pady=(0, 10))

        # --- Cieľ (Goal) ---
        self.goal_label = ctk.CTkLabel(self.container, text="Target (€):", font=("Courier New", 14, "bold"), text_color=actual_colors["font"])
        self.goal_label.pack(anchor="w", pady=(10, 5))
        self.goal_entry = ctk.CTkEntry(self.container, placeholder_text="5000", height=40, fg_color=actual_colors["bg1"], text_color=actual_colors["font"])
        self.goal_entry.pack(fill="x", pady=(0, 10))

        # --- Tlačidlo Uložiť ---
        self.save_btn = ctk.CTkButton(
            self.container, text="CREATE", font=("Courier New", 18, "bold"),
            fg_color=actual_colors["bg2"], hover_color=actual_colors["bg2"], height=50, text_color=actual_colors["font"],
            command=self.handle_save
        )
        self.save_btn.pack(fill="x", pady=30)

    def _toggle_goal(self, choice):
        if choice == "Budget":
            self.goal_label.pack_forget()
            self.goal_entry.pack_forget()
        else:
            self.goal_label.pack(anchor="w", pady=(10, 5), before=self.save_btn)
            self.goal_entry.pack(fill="x", pady=(0, 10), before=self.save_btn)

    def handle_save(self):
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
        self.on_cancel_callback()

class TransactionWindow(ctk.CTkToplevel):
    def __init__(self, parent, component, refresh_callback, actual_colors):
        super().__init__(parent)
        
        # 1. Window Setup
        self.width = 350
        self.height = 380 
        self.overrideredirect(True) 
        self.attributes("-topmost", True) 
        self.configure(fg_color=actual_colors["font"]) 
        
        self.component = component
        self.refresh_callback = refresh_callback

        # 2. THE MAIN CONTAINER
        self.main_border_frame = ctk.CTkFrame(
            self, 
            corner_radius=0, 
            border_width=2, 
            border_color=actual_colors["font"], 
            fg_color=actual_colors["bg2"],
        )
        self.main_border_frame.pack(fill="both", expand=True)

        
        
        self.trans_type_var = ctk.StringVar(value="Income")

        # The Border Frame
        self.button_border = ctk.CTkFrame(
            self.main_border_frame, 
            fg_color=actual_colors["font"], 
            corner_radius=8
        )
        self.button_border.pack(pady=(20, 10), padx=20)

        # The Segmented Button
        self.type_switch = ctk.CTkSegmentedButton(
            self.button_border, 
            values=["Income", "Expense"], 
            font=("Courier New", 16, "bold"),
            variable=self.trans_type_var,
            height=35,
            fg_color=actual_colors["bg1"], 
            selected_color=actual_colors["bg2"], 
            selected_hover_color=actual_colors["bg2"], 
            unselected_hover_color=actual_colors["bg1"], 
            unselected_color=actual_colors["bg1"],
            text_color=actual_colors["font"]
        )
        self.type_switch.pack(padx=2, pady=2)

        # 3. Form Container (Replaces Tabview)
        self.form_frame = ctk.CTkFrame(self.main_border_frame, fg_color=actual_colors["bg1"], corner_radius=12)
        self.form_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        # Setup the dynamic form
        self.setup_form(self.form_frame, actual_colors)

        # 4. Centering and Focus
        self.center_to_root(parent)
        self.grab_set() 

    def setup_form(self, container, actual_colors):
        # Amount
        ctk.CTkLabel(container, text="Amount:", font=("Courier New", 13, "bold"), text_color=actual_colors["font"]).pack(pady=(20, 0))
        self.amt_entry = ctk.CTkEntry(container, placeholder_text="0.00€", width=220, fg_color=actual_colors["bg1"], text_color=actual_colors["font"])
        self.amt_entry.pack(pady=5)

        # Note
        ctk.CTkLabel(container, text="Note:", font=("Courier New", 13, "bold"), text_color=actual_colors["font"]).pack(pady=(10, 0))
        self.note_entry = ctk.CTkEntry(container, placeholder_text="Description...", width=220, fg_color=actual_colors["bg1"], text_color=actual_colors["font"])
        self.note_entry.pack(pady=5)

        # --- Button Container ---
        button_frame = ctk.CTkFrame(container, fg_color="transparent")
        button_frame.pack(pady=25)

        # Save Button
        submit_btn = ctk.CTkButton(
            button_frame, text="Save", width=100,
            fg_color=actual_colors["green"], text_color="white",
            hover_color=actual_colors["green"],
            command=self.handle_save_wrapper 
        )
        submit_btn.pack(side="left", padx=10)

        # Cancel Button
        cancel_btn = ctk.CTkButton(
            button_frame, text="Cancel", width=100,
            fg_color=actual_colors["red"], text_color="white",
            hover_color=actual_colors["red"],
            command=self.destroy
        )
        cancel_btn.pack(side="left", padx=10)

    def handle_save_wrapper(self):
        
        choice = self.trans_type_var.get()
        t_type = TransactionType.INCOME if choice == "Income" else TransactionType.EXPENSE
        self.save_transaction(self.amt_entry, self.note_entry, t_type)

    def center_to_root(self, root):
        root.update_idletasks()
        root_x = root.winfo_x()
        root_y = root.winfo_y()
        root_width = root.winfo_width()
        root_height = root.winfo_height()

        spawn_x = (root_x + (root_width // 2) - (self.width // 2))
        spawn_y = (root_y + (root_height // 2) - (self.height // 2))
        self.geometry(f"{self.width}x{self.height}+{spawn_x}+{spawn_y}")


        

    def save_transaction(self, amt_entry, note_entry, trans_type):
        try:
            raw_val = amt_entry.get().replace('€', '').replace(',', '.').strip()
            amount = float(raw_val)
            note = note_entry.get() if note_entry.get() else "No note"
            
            
            new_amount = self.component.current_amount + (amount if (trans_type==TransactionType.INCOME) else -amount)
            
            new_tx = Transaction(amount, trans_type, new_amount, datetime.now(), note=note)
            self.component.add_transaction(new_tx)
            
            
            from data_manager import save_data
            import __main__ 
            save_data(__main__.financial_components) 
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
    def __init__(self, master, transactions, color, actual_colors, **kwargs):
        kwargs.setdefault("height", 250)
        kwargs.setdefault("bg", actual_colors["bg1"])
        kwargs.setdefault("highlightthickness", 0)
        super().__init__(master, **kwargs)
        
        self.transactions = transactions # Now expects a list of Transaction objects
        self.color = color
        self.actual_colors = actual_colors
        self.points_map = [] # To store (x, y, transaction_object)

        self.bind("<Configure>", lambda e: self.draw())
        self.bind("<Motion>", self.on_mouse_move)
        self.bind("<Leave>", lambda e: self.hide_tooltip())

    def draw(self):
        self.delete("all")
        self.points_map = []
        
        width = self.winfo_width()
        height = self.winfo_height()

        if width <= 1 or not self.transactions:
            self.create_text(width/2, height/2, text="No data", fill="gray", font=("Courier New", 12))
            return

        pad_l, pad_r, pad_t, pad_b = 60, 40, 40, 40
        
        # --- FIX: Create a virtual start point at 0 ---
        # Create a dummy transaction object for the start
        start_tx = Transaction(0, TransactionType.INCOME, 0, self.transactions[0].date, "Start")
        display_data = [start_tx] + self.transactions 

        # --- FIX: Ensure 0 is the minimum for the scale ---
        amounts = [t.amount for t in display_data]
        max_v = max(amounts)
        min_v = 0 # Force the bottom to be 0
        v_range = max_v if max_v != 0 else 1

        # Draw Grid
        steps = 4
        for i in range(steps + 1):
            y = pad_t + (i * (height - pad_t - pad_b) / steps)
            self.create_line(pad_l, y, width - pad_r, y, fill=self.actual_colors["bg2"], dash=(2, 2))
            val = max_v - (i * v_range / steps)
            self.create_text(pad_l - 10, y, text=f"{val:.0f}€", 
                             fill="gray", anchor="e", font=("Courier New", 10, "bold"))

        # Calculate Points
        points = []
        divisor = (len(display_data) - 1)
        for i, tx in enumerate(display_data):
            x = pad_l + (i * (width - pad_l - pad_r) / divisor)
            norm = (tx.amount - min_v) / v_range
            y = (height - pad_b) - (norm * (height - pad_t - pad_b))
            points.append((x, y, tx))

        # Draw Line
        if len(points) > 1:
            coords = [(p[0], p[1]) for p in points]
            self.create_line(coords, fill=self.color, width=3)
        
        # Draw Points (Skip drawing the dummy point 0 if you want it to look cleaner)
        for i, (x, y, tx) in enumerate(points):
            if i == 0: continue # Don't draw a circle for the "fake" 0 point
            self.create_oval(x-4, y-4, x+4, y+4, fill=self.color, outline="white", width=1)
            self.points_map.append((x, y, tx))

    def on_mouse_move(self, event):
        mouse_x, mouse_y = event.x, event.y
        closest_point = None
        min_dist = 15

        for px, py, tx in self.points_map:
            dist = ((mouse_x - px)**2 + (mouse_y - py)**2)**0.5
            if dist < min_dist:
                closest_point = (px, py, tx)
                break
        
        if closest_point:
            self.show_tooltip(*closest_point)
        else:
            self.hide_tooltip()

    def show_tooltip(self, x, y, tx):
        self.hide_tooltip()
        
        date_str = tx.date.strftime('%d.%m.%Y')
        amt_str = f"{tx.amount:.2f}€"
        note_str = (tx.note[:15] + '..') if len(tx.note) > 15 else tx.note
        full_text = f"{date_str}\n{amt_str}\n"

        tw, th = 110, 55
        cw, ch = self.winfo_width(), self.winfo_height()

        # Flip logic so it doesn't get cut off
        rx = x - tw - 15 if x + tw + 20 > cw else x + 15
        ry = y + 15 if y - th - 10 < 0 else y - th - 10

        self.create_rectangle(rx, ry, rx + tw, ry + th, 
                              fill=self.actual_colors["bg2"], outline=self.actual_colors["font"], 
                              tags="tooltip", width=1)
        
        self.create_text(rx + 8, ry + 8, text=full_text, fill=self.actual_colors["font"], 
                         font=("Courier New", 10, "bold"), anchor="nw", tags="tooltip")

    def hide_tooltip(self):
        self.delete("tooltip")
class CombinedGraph(ctk.CTkCanvas):
    def __init__(self, master, transactions, actual_colors, **kwargs):
        kwargs.setdefault("height", 400)
        kwargs.setdefault("bg", actual_colors["bg1"]) # Match theme background
        kwargs.setdefault("highlightthickness", 0)
        super().__init__(master, **kwargs)
        
        self.transactions = transactions
        self.actual_colors = actual_colors
        self.points_map = [] # To store (x, y, transaction_object)
        
        # Bind events for interactivity
        self.bind("<Configure>", lambda e: self.draw(actual_colors))
        self.bind("<Motion>", self.on_mouse_move)
        self.bind("<Leave>", lambda e: self.hide_tooltip())

    def draw(self, actual_colors):
        self.delete("all")
        self.points_map = []
        
        width = self.winfo_width()
        height = self.winfo_height()

        if width <= 1 or not self.transactions:
            self.create_text(width/2, height/2, text="No transactions", fill="gray")
            return

        pad_l, pad_r, pad_t, pad_b = 60, 40, 40, 40
        
        # --- FIX: Prepend a 0 balance start point ---
        start_tx = Transaction(0, TransactionType.INCOME, 0, self.transactions[0].date, "Opening")
        display_data = [start_tx] + self.transactions

        # --- FIX: Scale includes 0 ---
        amounts = [t.current_amount for t in display_data]
        max_v = max(amounts)
        min_v = min(0, min(amounts)) # Handle negative balance if it exists
        v_range = (max_v - min_v) if max_v != min_v else 1

        # Draw Grid Lines
        for i in range(5):
            y = pad_t + (i * (height - pad_t - pad_b) / 4)
            self.create_line(pad_l, y, width - pad_r, y, fill=actual_colors["bg2"], dash=(2, 2))
            val = max_v - (i * v_range / 4)
            self.create_text(pad_l - 10, y, text=f"{val:.0f}€", fill=actual_colors["bg2"], anchor="e", font=("Courier New", 11, "bold"))

        # Calculate Points
        points = []
        divisor = (len(display_data) - 1)
        for i, tx in enumerate(display_data):
            x = pad_l + (i * (width - pad_l - pad_r) / divisor)
            norm = (tx.current_amount - min_v) / v_range
            y = (height - pad_b) - (norm * (height - pad_t - pad_b))
            points.append((x, y, tx))

        # Draw connecting lines
        if len(points) > 1:
            for i in range(1, len(points)):
                p1, p2 = points[i-1], points[i]
                # If it's the first segment (from 0), use neutral gray or font color
                line_color = (self.actual_colors["green"] if p2[2].type == TransactionType.INCOME else self.actual_colors["red"])
                self.create_line(p1[0], p1[1], p2[0], p2[1], fill=line_color, width=3)

        # Draw Points (Skip the virtual 0 point)
        for i, (x, y, tx) in enumerate(points):
            if i == 0: continue 
            color = self.actual_colors["green"] if tx.type == TransactionType.INCOME else self.actual_colors["red"]
            self.create_oval(x-5, y-5, x+5, y+5, fill=color, outline="white", width=1, tags="points")
            self.points_map.append((x, y, tx))

    def on_mouse_move(self, event):
        """Detects if the mouse is near a point and shows tooltip."""
        mouse_x, mouse_y = event.x, event.y
        closest_point = None
        min_dist = 15 # Sensitivity radius in pixels

        for px, py, tx in self.points_map:
            # Simple Pythagorean distance
            dist = ((mouse_x - px)**2 + (mouse_y - py)**2)**0.5
            if dist < min_dist:
                closest_point = (px, py, tx)
                break
        
        if closest_point:
            self.show_tooltip(*closest_point)
        else:
            self.hide_tooltip()

    def show_tooltip(self, x, y, tx):
        self.hide_tooltip()
        
        # 1. Tooltip Content
        date_str = tx.date.strftime('%d.%m.%Y')
        amt_str = f"{'+' if tx.type == TransactionType.INCOME else '-'}{tx.amount:.2f}€"
        bal_str = f"Bal: {tx.current_amount:.0f}€"
        full_text = f"{date_str}\n{amt_str}\n{bal_str}"

        # 2. Tooltip Dimensions
        tw, th = 110, 60
        
        # 3. Dynamic Positioning (Bounds Checking)
        canvas_w = self.winfo_width()
        canvas_h = self.winfo_height()

        # Horizontal positioning: Flip to left if near right edge
        if x + tw + 20 > canvas_w:
            rect_x1 = x - tw - 15
        else:
            rect_x1 = x + 15
        
        # Vertical positioning: Flip to bottom if near top edge
        if y - th - 10 < 0:
            rect_y1 = y + 15
        else:
            rect_y1 = y - th - 10

        rect_x2 = rect_x1 + tw
        rect_y2 = rect_y1 + th

        # 4. Draw Tooltip Background (Rectangle)
        self.create_rectangle(rect_x1, rect_y1, rect_x2, rect_y2, 
                              fill=self.actual_colors["bg2"], 
                              outline=self.actual_colors["font"], 
                              tags="tooltip", width=1)
        
        # 5. Draw Tooltip Text
        # We anchor "nw" (North West) so text starts at the top-left of the rectangle
        self.create_text(rect_x1 + 8, rect_y1 + 8, 
                         text=full_text, fill=self.actual_colors["font"], 
                         font=("Courier New", 10, "bold"), 
                         anchor="nw", tags="tooltip")

    def hide_tooltip(self):
        self.delete("tooltip")