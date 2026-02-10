import customtkinter as ctk

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Scrollable Drill-down Example")
        self.geometry("400x500")

        # Sample data
        self.data = {
            "User 1": ["Email: user1@example.com", "ID: 001", "Status: Active", "Last Login: 2 hours ago"],
            "User 2": ["Email: user2@example.com", "ID: 002", "Status: Inactive", "Last Login: 5 days ago"],
            "User 3": ["Email: user3@example.com", "ID: 003", "Status: Active", "Last Login: 10 mins ago"],
        }

        # Create the Scrollable Frame
        self.scrollable_frame = ctk.CTkScrollableFrame(self, label_text="Data List")
        self.scrollable_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Show the initial list
        self.show_main_list()

    def clear_frame(self):
        """Removes all widgets from the scrollable frame"""
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

    def show_main_list(self):
        """Populates the frame with a list of clickable items"""
        self.clear_frame()
        self.scrollable_frame.configure(label_text="Select a User")

        for name in self.data.keys():
            # Create a button for each element
            # We use lambda name=name to capture the current value of 'name' in the loop
            btn = ctk.CTkButton(
                self.scrollable_frame, 
                text=name, 
                command=lambda n=name: self.show_details(n)
            )
            btn.pack(fill="x", padx=10, pady=5)

    def show_details(self, name):
        """Clears the frame and fills it with specific data from the clicked element"""
        self.clear_frame()
        self.scrollable_frame.configure(label_text=f"Details: {name}")

        # Add a 'Back' button to return to the list
        back_btn = ctk.CTkButton(self.scrollable_frame, text="← Back", fg_color="gray", command=self.show_main_list)
        back_btn.pack(pady=(0, 20))

        # Fill with detailed data
        details = self.data[name]
        for info in details:
            label = ctk.CTkLabel(self.scrollable_frame, text=info, font=("Arial", 14))
            label.pack(anchor="w", padx=20, pady=2)

if __name__ == "__main__":
    app = App()
    app.mainloop()