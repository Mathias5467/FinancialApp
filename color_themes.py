color_index = 1

# --- Color themes ---
color_themes = [{"bg1": "#2E2A33", "bg2": "#5B5166", "font": "#D6CFDC","green": "#72bd39", "red": "#FF8F8F"}, # Withered Plum (Dark)
                {"bg1": "#343E3D", "bg2": "#607466", "font": "#AEDCC0","green": "#72bd39", "red": "#FF8F8F"}, # Forest Green (Dark)
                {"bg1": "#2D3436", "bg2": "#4B5E66", "font": "#D1E2E4","green": "#72bd39", "red": "#FF8F8F"}, # Midnight Slate (Dark)
                {"bg1": "#363533", "bg2": "#615F5B", "font": "#E3E1DC","green": "#72bd39", "red": "#FF8F8F"}, # Ancient Stone (Dark)
                {"bg1": "#1F2E2E", "bg2": "#415C5C", "font": "#B8D9D9","green": "#72bd39", "red": "#FF8F8F"}, # Deep Ocean (Dark)
                {"bg1": "#3D3434", "bg2": "#746060", "font": "#DCCAA8","green": "#72bd39", "red": "#FF8F8F"}, # Dark Auburn (Dark)
                
                # --- Light Mode Themes ---
                {"bg1": "#F0F9F4", "bg2": "#C8E6D1", "font": "#1B3022", "green": "#489b0d", "red": "#AF0D0D"}, # Sharp Sage (Vibrant Green)
                {"bg1": "#F2F8FA", "bg2": "#BDD1DB", "font": "#1A252B", "green": "#489b0d", "red": "#AF0D0D"}, # Bright Slate (Vibrant Blue)
                {"bg1": "#FAF5FF", "bg2": "#DED0EE", "font": "#2E1A47", "green": "#489b0d", "red": "#AF0D0D"}, # Vivid Lavender (Vibrant Purple)
                {"bg1": "#FFFBF5", "bg2": "#EADBC8", "font": "#3B2F21", "green": "#489b0d", "red": "#AF0D0D"}, # Warm Sand (Vibrant Neutral)
                {"bg1": "#E6FFFF", "bg2": "#A5E5E5", "font": "#0B2B2B", "green": "#489b0d", "red": "#AF0D0D"}, # Electric Mint (Vibrant Teal)
                {"bg1": "#FFF5F2", "bg2": "#EBCDC3", "font": "#451F1F", "green": "#489b0d", "red": "#AF0D0D"}  # Rose Clay (Vibrant Auburn)
                ]


def set_color_index(new_index):
    global color_index
    if (new_index >= 0 and new_index < len(color_themes)):
        color_index = new_index
