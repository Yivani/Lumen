<<<<<<< HEAD
import customtkinter as ctk
import os
import json
import shutil
import math
import sys
from tkinter import filedialog

# --- CONFIG & COLORS ---
COL_TEXT_LIGHT = "#dceabd"    
COL_TEXT_DARK  = "#141614"    
COL_ACCENT_GOLD= "#d9b84f"    

COL_BG_ROOT    = "#141614"    
COL_BG_PANEL   = "#1F221E"    
COL_BG_INPUT   = "#232621"    
COL_BORDER     = "#45483c"    

# --- CURRENCIES ---
C_REN = "#d9b84f"
C_EXO = "#ceb9de"
C_RED = "#f22e00"
C_BIO = "#00b57c"
C_LIC = "#01f5ff"
C_REF = "#FFFFFF"

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

# --- ICON BUNDLING HELPER ---
def resource_path(relative_path):
    """Get absolute path to resource file. Works for both development and PyInstaller builds."""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# --- THEMED POPUP SYSTEM ---
class ThemePopup(ctk.CTkToplevel):
    def __init__(self, title, message, color=COL_ACCENT_GOLD):
        super().__init__()
        self.geometry("420x240")
        self.title(title.upper())
        self.configure(fg_color=COL_BG_ROOT)
        self.resizable(False, False)
        self.overrideredirect(True) 

        # Center popup window on screen
        self.update_idletasks()
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = (ws/2) - (420/2)
        y = (hs/2) - (240/2)
        self.geometry('%dx%d+%d+%d' % (420, 240, x, y))
        self.attributes("-topmost", True)

        main_frame = ctk.CTkFrame(self, fg_color=COL_BG_PANEL, border_width=2, border_color=color, corner_radius=0)
        main_frame.pack(fill="both", expand=True, padx=2, pady=2)

        ctk.CTkLabel(main_frame, text=title.upper(), font=("Impact", 24), text_color=color).pack(pady=(25, 10))
        ctk.CTkLabel(main_frame, text=message, font=("Arial", 13), text_color=COL_TEXT_LIGHT, wraplength=380).pack(pady=10)
        
        ctk.CTkButton(
            main_frame, text="ACKNOWLEDGE", command=self.destroy,
            fg_color=color, text_color=COL_TEXT_DARK, hover_color="#b59840",
            font=("Arial", 12, "bold"), width=140, height=40, corner_radius=2
        ).pack(side="bottom", pady=25)
        self.grab_set()

class LumenIcarusEditor(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- WINDOW SETUP ---
        self.title("LUMEN EDITOR [v1.0]")
        w_width, w_height = 850, 850 
        s_width = self.winfo_screenwidth()
        s_height = self.winfo_screenheight()
        x_pos = int((s_width / 2) - (w_width / 2))
        y_pos = int((s_height / 2) - (w_height / 2))
        self.geometry(f"{w_width}x{w_height}+{x_pos}+{y_pos}")
        self.minsize(700, 700)
        self.configure(fg_color=COL_BG_ROOT)

        # Load application icon (works for both development and PyInstaller builds)
        icon_file = resource_path("logo.ico")
        if os.path.exists(icon_file):
            try: self.iconbitmap(icon_file)
            except: pass

        # Initialize application state
        self.profiles_map = self.scan_for_profiles() 
        self.current_folder_path = None
        self.profile_data = {}
        self.char_container = None 
        self.char_key_or_index = None
        self.char_is_encoded_string = False 
        self.char_is_nested_list = False    
        self.entries = {}
        self.xp_entry_ref = None
        self.lvl_entry_ref = None
        self.progress_bar_ref = None
        self.progress_label_ref = None
        
        self.create_widgets()
        
        if self.profiles_map:
            first_id = list(self.profiles_map.keys())[0]
            self.profile_dropdown.set(first_id)
            self.change_profile(first_id)
        else:
            self.status_label.configure(text="NO PROFILE - SELECT MANUALLY", text_color="#FF5555")
            self.btn_save.configure(state="disabled")
            self.show_message("NO PROFILE FOUND", "Could not auto-detect profiles.\nPlease click [ BROWSE ] and select your PlayerData folder manually.", "#FF5555")

    def show_message(self, title, msg, color=COL_ACCENT_GOLD):
        """Display a themed popup message dialog."""
        ThemePopup(title, msg, color)

    def scan_for_profiles(self):
        """Scan default Icarus installation directory for player profiles."""
        appdata = os.getenv('LOCALAPPDATA')
        if not appdata: return {}
        base_path = os.path.join(appdata, 'Icarus', 'Saved', 'PlayerData')
        profiles = {}
        if os.path.exists(base_path):
            for folder in os.listdir(base_path):
                full_path = os.path.join(base_path, folder)
                if os.path.isdir(full_path) and folder.isdigit():
                    profiles[folder] = full_path
        return profiles

    def browse_folder(self):
        """Open file dialog to manually select a player data folder."""
        folder_selected = filedialog.askdirectory(title="SELECT ICARUS PLAYER DATA FOLDER")
        if folder_selected:
            p_check = os.path.join(folder_selected, "Profile.json")
            if os.path.exists(p_check):
                folder_name = os.path.basename(folder_selected)
                self.profiles_map[folder_name] = folder_selected
                self.profile_dropdown.configure(values=list(self.profiles_map.keys()))
                self.profile_dropdown.set(folder_name)
                self.current_folder_path = folder_selected
                self.load_data()
                self.btn_save.configure(state="normal")
                self.show_message("SUCCESS", f"Profile loaded successfully:\n{folder_name}")
            else:
                self.show_message("INVALID FOLDER", "Folder must contain Profile.json!", "#FF5555")

    def create_widgets(self):
        self.header_frame = ctk.CTkFrame(self, fg_color=COL_BG_PANEL, border_width=1, border_color=COL_BORDER, corner_radius=0, height=80)
        self.header_frame.pack(fill="x", side="top", padx=1, pady=1)
        ctk.CTkLabel(self.header_frame, text="LUMEN // EDITOR", font=("Impact", 28), text_color=COL_TEXT_LIGHT).pack(side="left", padx=30, pady=20)

        ctrl_frame = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        ctrl_frame.pack(side="right", padx=30)

        self.btn_browse = ctk.CTkButton(
            ctrl_frame, text="[ BROWSE ]", width=100, command=self.browse_folder,
            fg_color=COL_BG_INPUT, hover_color=COL_BORDER, border_width=1, border_color=COL_BORDER, text_color=COL_TEXT_LIGHT
        )
        self.btn_browse.pack(side="right", padx=10)

        self.profile_dropdown = ctk.CTkOptionMenu(
            ctrl_frame, values=list(self.profiles_map.keys()) if self.profiles_map else ["NO PROFILE"],
            command=self.change_profile, width=200, fg_color=COL_BG_INPUT, button_color=COL_BORDER,
            button_hover_color=COL_ACCENT_GOLD, text_color=COL_TEXT_LIGHT, dropdown_fg_color=COL_BG_PANEL, dropdown_text_color=COL_TEXT_LIGHT,
            corner_radius=2
        )
        self.profile_dropdown.pack(side="right", padx=5)
        ctk.CTkLabel(ctrl_frame, text="ID:", font=("Arial", 10, "bold"), text_color=COL_BORDER).pack(side="right", padx=5)

        self.frame = ctk.CTkFrame(self, width=600, corner_radius=0, fg_color="transparent")
        self.frame.pack(pady=10, padx=0, fill="both", expand=True)

        self.footer_frame = ctk.CTkFrame(self, fg_color=COL_BG_PANEL, border_width=1, border_color=COL_BORDER, corner_radius=0, height=90)
        self.footer_frame.pack(fill="x", side="bottom", padx=1, pady=1)

        self.status_label = ctk.CTkLabel(self.footer_frame, text="WAITING...", font=("Consolas", 12), text_color=COL_BORDER)
        self.status_label.pack(side="left", padx=30)

        self.btn_save = ctk.CTkButton(
            self.footer_frame, text="[ SAVE & APPLY ]", command=self.save_data, width=220, height=45,
            font=("Arial", 13, "bold"), fg_color=COL_ACCENT_GOLD, hover_color="#b59840", text_color=COL_TEXT_DARK, corner_radius=2
        )
        self.btn_save.pack(side="right", padx=30, pady=20)
        
        self.btn_refresh = ctk.CTkButton(
            self.footer_frame, text="RELOAD", command=self.refresh_current_profile, width=100, height=45,
            font=("Arial", 12, "bold"), fg_color=COL_BG_INPUT, hover_color=COL_BORDER, text_color=COL_TEXT_LIGHT, border_width=1, border_color=COL_BORDER, corner_radius=2
        )
        self.btn_refresh.pack(side="right", padx=10)

    def change_profile(self, selected_id):
        """Switch to a different player profile."""
        if selected_id in self.profiles_map:
            self.current_folder_path = self.profiles_map[selected_id]
            self.load_data()
        else:
            self.current_folder_path = None

    def refresh_current_profile(self):
        """Reload data from the currently selected profile."""
        if self.current_folder_path:
            self.load_data()
            self.status_label.configure(text="DATA RELOADED", text_color=C_LIC)

    def clear_ui(self):
        """Remove all widgets from the main content frame."""
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.entries.clear()

    def add_section_header(self, text):
        """Create a styled section header with accent bar."""
        container = ctk.CTkFrame(self.frame, fg_color="transparent")
        container.pack(fill="x", pady=(25, 5), padx=30)
        ctk.CTkFrame(container, width=3, height=18, fg_color=COL_ACCENT_GOLD, corner_radius=0).pack(side="left")
        ctk.CTkLabel(container, text=text, font=("Arial", 16, "bold"), text_color=COL_TEXT_LIGHT).pack(side="left", padx=10)
        ctk.CTkFrame(self.frame, height=1, fg_color=COL_BORDER, corner_radius=0).pack(fill="x", padx=30, pady=0)

    def add_input_field(self, label_text, key_id, value, section, icon_color=None):
        """Create a labeled input field with optional colored accent bar."""
        row = ctk.CTkFrame(self.frame, fg_color=COL_BG_PANEL, border_width=1, border_color=COL_BORDER, corner_radius=2)
        row.pack(fill="x", pady=4, padx=30)
        
        if icon_color: ctk.CTkFrame(row, width=4, height=45, corner_radius=0, fg_color=icon_color).pack(side="left")
        else: ctk.CTkFrame(row, width=4, height=45, corner_radius=0, fg_color="transparent").pack(side="left")

        ctk.CTkLabel(row, text=label_text.upper(), font=("Arial", 11, "bold"), text_color=COL_TEXT_LIGHT, anchor="w", width=220).pack(side="left", padx=15)
        
        entry = ctk.CTkEntry(
            row, font=("Consolas", 15), fg_color=COL_BG_INPUT, border_width=0, corner_radius=0,
            text_color=COL_TEXT_LIGHT, justify="right"
        )
        val_str = str(value) if value is not None else "0"
        entry.insert(0, val_str)
        entry.pack(side="right", padx=15, pady=10, fill="x", expand=True)
        
        self.entries[f"{section}|{key_id}"] = entry
        return entry

    def add_level_manager(self, current_xp, section):
        """Create the level/XP management widget with progress bar and calculators."""
        container = ctk.CTkFrame(self.frame, fg_color=COL_BG_PANEL, border_width=1, border_color=COL_BORDER, corner_radius=2)
        container.pack(fill="x", pady=5, padx=30)
        
        head = ctk.CTkFrame(container, fg_color="transparent")
        head.pack(fill="x", padx=15, pady=10)
        ctk.CTkLabel(head, text="LEVEL MANAGER", font=("Arial", 11, "bold"), text_color=COL_ACCENT_GOLD).pack(side="left")

        controls = ctk.CTkFrame(container, fg_color="transparent")
        controls.pack(fill="x", padx=10, pady=5)
        
        left_box = ctk.CTkFrame(controls, fg_color="transparent")
        left_box.pack(side="left", fill="x", expand=True)
        ctk.CTkLabel(left_box, text="TARGET LEVEL", font=("Arial", 9, "bold"), text_color=COL_BORDER).pack(anchor="w")
        self.lvl_entry_ref = ctk.CTkEntry(left_box, width=60, font=("Consolas", 14), fg_color=COL_BG_INPUT, border_width=0, justify="center", text_color=COL_TEXT_LIGHT)
        self.lvl_entry_ref.pack(side="left", pady=2)
        ctk.CTkButton(left_box, text="CALC XP ->", width=90, command=self.calc_xp_from_lvl, corner_radius=2, fg_color=COL_BORDER, hover_color=COL_BG_INPUT, text_color=COL_TEXT_LIGHT).pack(side="left", padx=5)

        right_box = ctk.CTkFrame(controls, fg_color="transparent")
        right_box.pack(side="right", fill="x", expand=True)
        ctk.CTkLabel(right_box, text="CUSTOM XP", font=("Arial", 9, "bold"), text_color=COL_BORDER).pack(anchor="w")
        self.xp_entry_ref = ctk.CTkEntry(right_box, font=("Consolas", 14), fg_color=COL_BG_INPUT, border_width=0, justify="right", text_color=COL_TEXT_LIGHT)
        self.xp_entry_ref.insert(0, str(current_xp))
        self.xp_entry_ref.pack(side="left", fill="x", expand=True, pady=2)
        ctk.CTkButton(right_box, text="<- GET LVL", width=90, command=self.calc_lvl_from_xp, corner_radius=2, fg_color=COL_BORDER, hover_color=COL_BG_INPUT, text_color=COL_TEXT_LIGHT).pack(side="left", padx=5)

        self.entries[f"{section}|XP"] = self.xp_entry_ref

        bar_frame = ctk.CTkFrame(container, fg_color="transparent")
        bar_frame.pack(fill="x", padx=15, pady=(15, 20))
        self.progress_label_ref = ctk.CTkLabel(bar_frame, text="LEVEL PROGRESS", font=("Arial", 10, "bold"), text_color=COL_TEXT_LIGHT, anchor="w")
        self.progress_label_ref.pack(fill="x", pady=(0, 4))
        self.progress_bar_ref = ctk.CTkProgressBar(bar_frame, height=14, corner_radius=0, fg_color=COL_BORDER, progress_color=COL_TEXT_LIGHT)
        self.progress_bar_ref.set(0)
        self.progress_bar_ref.pack(fill="x")
        self.update_progress_visuals(current_xp)

    def calc_xp_from_lvl(self):
        """Calculate required XP for a given level using Icarus formula: XP = 1570 * level²"""
        try:
            lvl = int(self.lvl_entry_ref.get())
            if lvl < 1: lvl = 1
            if lvl > 150: lvl = 150
            new_xp = int(1570 * (lvl ** 2))
            
            self.xp_entry_ref.delete(0, "end")
            self.xp_entry_ref.insert(0, str(new_xp))
            self.update_progress_visuals(new_xp)
            self.status_label.configure(text=f"SET TO LEVEL {lvl}", text_color=COL_TEXT_LIGHT)
        except ValueError:
            pass

    def calc_lvl_from_xp(self):
        """Calculate level from XP using inverse formula: level = √(XP / 1570)"""
        try:
            raw_xp = int(self.xp_entry_ref.get())
            lvl = int(math.sqrt(raw_xp / 1570))
            if lvl < 1: lvl = 1
            self.lvl_entry_ref.delete(0, "end")
            self.lvl_entry_ref.insert(0, str(lvl))
            self.update_progress_visuals(raw_xp)
            self.status_label.configure(text=f"XP MATCHES LEVEL {lvl}", text_color=COL_TEXT_LIGHT)
        except ValueError:
            pass

    def update_progress_visuals(self, current_xp):
        """Update progress bar and label to show current level progress."""
        try:
            current_xp = int(current_xp)
            current_lvl = int(math.sqrt(current_xp / 1570))
            xp_start_of_lvl = int(1570 * (current_lvl ** 2))
            xp_start_of_next = int(1570 * ((current_lvl + 1) ** 2))
            range_span = xp_start_of_next - xp_start_of_lvl
            if range_span <= 0: range_span = 1
            progress_val = (current_xp - xp_start_of_lvl) / range_span
            if progress_val < 0: progress_val = 0
            if progress_val > 1: progress_val = 1
            self.progress_bar_ref.set(progress_val)
            pct = int(progress_val * 100)
            txt = f"LEVEL {current_lvl}  >>  {pct}%  >>  LEVEL {current_lvl + 1}"
            self.progress_label_ref.configure(text=txt)
        except:
            pass

    def load_data(self):
        """Load and display profile and character data from JSON files."""
        if not self.current_folder_path or not os.path.exists(self.current_folder_path): return
        self.clear_ui()

        # Load Profile.json (account wallet/currencies)
        p_path = os.path.join(self.current_folder_path, 'Profile.json')
        if os.path.exists(p_path):
            try:
                with open(p_path, 'r', encoding='utf-8') as f:
                    self.profile_data = json.load(f)
                self.add_section_header("ACCOUNT WALLET")
                
                currency_config = {
                    "Refund":     {"label": "RESPEC POINTS", "color": C_REF},
                    "Credits":    {"label": "REN", "color": C_REN},
                    "Exotic1":    {"label": "EXOTICS", "color": C_EXO},
                    "Exotic_Red": {"label": "STABILIZED", "color": C_RED},
                    "Biomass":    {"label": "LEGENDARY BIOMASS", "color": C_BIO},
                    "licence":    {"label": "LEGENDARY LICENSE", "color": C_LIC}, 
                }
                meta = self.profile_data.get("MetaResources", [])
                
                # Track which currencies have been added to avoid duplicates
                added_labels = [] 
                
                for item in meta:
                    key = item.get("MetaRow")
                    if key in currency_config:
                        conf = currency_config[key]
                        if conf["label"] not in added_labels:
                            self.add_input_field(conf["label"], key, item.get("Count", 0), "PROFILE", icon_color=conf["color"])
                            added_labels.append(conf["label"])
                
                # Add missing currencies with zero value
                for key, conf in currency_config.items():
                    if conf["label"] not in added_labels:
                        self.add_input_field(conf["label"], key, 0, "PROFILE_NEW", icon_color=conf["color"])
                        added_labels.append(conf["label"])

            except Exception as e:
                self.show_message("ERROR", f"Failed to load Profile:\n{e}", "#FF5555")

        # Load Characters.json (character XP and stats)
        c_path = os.path.join(self.current_folder_path, 'Characters.json')
        if os.path.exists(c_path):
            try:
                with open(c_path, 'r', encoding='utf-8') as f:
                    container = json.load(f)
                self.char_container = container
                raw_char_data = None
                
                # Handle different JSON structure formats (list or dict)
                if isinstance(container, list) and len(container) > 0:
                    self.char_key_or_index = 0
                    raw_char_data = container[0]
                elif isinstance(container, dict) and len(container) > 0:
                    first_key = next(iter(container))
                    self.char_key_or_index = first_key
                    raw_char_data = container[first_key]
                
                # Handle nested list structure
                if isinstance(raw_char_data, list) and len(raw_char_data) > 0:
                    raw_char_data = raw_char_data[0]
                    self.char_is_nested_list = True
                else:
                    self.char_is_nested_list = False
                
                # Parse character data (may be JSON string or dict)
                final_char_obj = {}
                if isinstance(raw_char_data, str):
                    try: 
                        final_char_obj = json.loads(raw_char_data)
                        self.char_is_encoded_string = True
                    except: 
                        pass
                elif isinstance(raw_char_data, dict):
                    final_char_obj = raw_char_data
                    self.char_is_encoded_string = False
                
                if final_char_obj:
                    name = final_char_obj.get("CharacterName", "UNKNOWN").upper()
                    self.add_section_header(f"CHARACTER: {name}")
                    current_xp = final_char_obj.get("XP", 0)
                    self.add_level_manager(current_xp, "CHAR")
                    try:
                        lvl_calc = int(math.sqrt(current_xp / 1570))
                        if self.lvl_entry_ref:
                            self.lvl_entry_ref.delete(0, "end")
                            self.lvl_entry_ref.insert(0, str(lvl_calc))
                    except: pass
            except Exception as e:
                self.show_message("ERROR", f"Failed to load Characters:\n{e}", "#FF5555")

        self.status_label.configure(text=f"CONNECTED: {os.path.basename(self.current_folder_path)}", text_color=C_BIO)

    def save_data(self):
        """Save modified data to JSON files with automatic backup creation."""
        if not self.current_folder_path: return
        try:
            p_path = os.path.join(self.current_folder_path, 'Profile.json')
            if os.path.exists(p_path):
                # Create backup before modifying
                shutil.copy(p_path, p_path + ".backup") 
                # Update existing currency values
                meta = self.profile_data.get("MetaResources", [])
                for key_full, entry in list(self.entries.items()):
                    section, r_key = key_full.split("|")
                    try: 
                        val = int(entry.get())
                    except: 
                        continue
                    if section == "PROFILE":
                        # Update existing currency
                        for item in meta:
                            if item["MetaRow"] == r_key: 
                                item["Count"] = val
                    elif section == "PROFILE_NEW" and val > 0:
                        # Add new currency entry
                        meta.append({"MetaRow": r_key, "Count": val})
                self.profile_data["MetaResources"] = meta
                with open(p_path, 'w', encoding='utf-8') as f: json.dump(self.profile_data, f, indent=4)

            c_path = os.path.join(self.current_folder_path, 'Characters.json')
            if self.char_container is not None and os.path.exists(c_path):
                # Create backup before modifying
                shutil.copy(c_path, c_path + ".backup")
                
                # Extract character data using stored structure info
                raw_data = self.char_container[self.char_key_or_index]
                if self.char_is_nested_list and isinstance(raw_data, list): 
                    item_to_edit = raw_data[0]
                else: 
                    item_to_edit = raw_data
                
                # Parse character object (may be JSON string or dict)
                char_obj = {}
                if self.char_is_encoded_string and isinstance(item_to_edit, str): 
                    char_obj = json.loads(item_to_edit)
                elif isinstance(item_to_edit, dict): 
                    char_obj = item_to_edit
                
                # Apply user changes to character data
                for key_full, entry in list(self.entries.items()):
                    section, r_key = key_full.split("|")
                    if section == "CHAR":
                        try: 
                            char_obj[r_key] = int(entry.get())
                        except: 
                            pass
                        
                # Reconstruct character data in original format
                final_element = char_obj
                if self.char_is_encoded_string: 
                    final_element = json.dumps(char_obj)
                if self.char_is_nested_list: 
                    self.char_container[self.char_key_or_index][0] = final_element
                else: 
                    self.char_container[self.char_key_or_index] = final_element
                with open(c_path, 'w', encoding='utf-8') as f: json.dump(self.char_container, f, indent=4)

            self.status_label.configure(text="SUCCESSFUL WRITE", text_color=C_BIO)
            self.show_message("SUCCESS", "Data saved successfully!\n\n(Restart game to see changes.)", C_BIO)

        except PermissionError:
             self.show_message("SAVE FAILED", "File is locked by Icarus.\nPlease close the game.", "#FF5555")
        except Exception as e:
            self.show_message("ERROR", f"Error saving data:\n{e}", "#FF5555")

if __name__ == "__main__":
    app = LumenIcarusEditor()
=======
import customtkinter as ctk
import os
import json
import shutil
import math
import sys
from tkinter import filedialog

# --- CONFIG & COLORS ---
COL_TEXT_LIGHT = "#dceabd"    
COL_TEXT_DARK  = "#141614"    
COL_ACCENT_GOLD= "#d9b84f"    

COL_BG_ROOT    = "#141614"    
COL_BG_PANEL   = "#1F221E"    
COL_BG_INPUT   = "#232621"    
COL_BORDER     = "#45483c"    

# --- CURRENCIES ---
C_REN = "#d9b84f"
C_EXO = "#ceb9de"
C_RED = "#f22e00"
C_BIO = "#00b57c"
C_LIC = "#01f5ff"
C_REF = "#FFFFFF"

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

# --- ICON BUNDLING HELPER ---
def resource_path(relative_path):
    """Get absolute path to resource file. Works for both development and PyInstaller builds."""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# --- THEMED POPUP SYSTEM ---
class ThemePopup(ctk.CTkToplevel):
    def __init__(self, title, message, color=COL_ACCENT_GOLD):
        super().__init__()
        self.geometry("420x240")
        self.title(title.upper())
        self.configure(fg_color=COL_BG_ROOT)
        self.resizable(False, False)
        self.overrideredirect(True) 

        # Center popup window on screen
        self.update_idletasks()
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = (ws/2) - (420/2)
        y = (hs/2) - (240/2)
        self.geometry('%dx%d+%d+%d' % (420, 240, x, y))
        self.attributes("-topmost", True)

        main_frame = ctk.CTkFrame(self, fg_color=COL_BG_PANEL, border_width=2, border_color=color, corner_radius=0)
        main_frame.pack(fill="both", expand=True, padx=2, pady=2)

        ctk.CTkLabel(main_frame, text=title.upper(), font=("Impact", 24), text_color=color).pack(pady=(25, 10))
        ctk.CTkLabel(main_frame, text=message, font=("Arial", 13), text_color=COL_TEXT_LIGHT, wraplength=380).pack(pady=10)
        
        ctk.CTkButton(
            main_frame, text="ACKNOWLEDGE", command=self.destroy,
            fg_color=color, text_color=COL_TEXT_DARK, hover_color="#b59840",
            font=("Arial", 12, "bold"), width=140, height=40, corner_radius=2
        ).pack(side="bottom", pady=25)
        self.grab_set()

class LumenIcarusEditor(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- WINDOW SETUP ---
        self.title("LUMEN EDITOR [v1.0]")
        w_width, w_height = 850, 850 
        s_width = self.winfo_screenwidth()
        s_height = self.winfo_screenheight()
        x_pos = int((s_width / 2) - (w_width / 2))
        y_pos = int((s_height / 2) - (w_height / 2))
        self.geometry(f"{w_width}x{w_height}+{x_pos}+{y_pos}")
        self.minsize(700, 700)
        self.configure(fg_color=COL_BG_ROOT)

        # Load application icon (works for both development and PyInstaller builds)
        icon_file = resource_path("logo.ico")
        if os.path.exists(icon_file):
            try: self.iconbitmap(icon_file)
            except: pass

        # Initialize application state
        self.profiles_map = self.scan_for_profiles() 
        self.current_folder_path = None
        self.profile_data = {}
        self.char_container = None 
        self.char_key_or_index = None
        self.char_is_encoded_string = False 
        self.char_is_nested_list = False    
        self.entries = {}
        self.xp_entry_ref = None
        self.lvl_entry_ref = None
        self.progress_bar_ref = None
        self.progress_label_ref = None
        
        self.create_widgets()
        
        if self.profiles_map:
            first_id = list(self.profiles_map.keys())[0]
            self.profile_dropdown.set(first_id)
            self.change_profile(first_id)
        else:
            self.status_label.configure(text="NO PROFILE - SELECT MANUALLY", text_color="#FF5555")
            self.btn_save.configure(state="disabled")
            self.show_message("NO PROFILE FOUND", "Could not auto-detect profiles.\nPlease click [ BROWSE ] and select your PlayerData folder manually.", "#FF5555")

    def show_message(self, title, msg, color=COL_ACCENT_GOLD):
        """Display a themed popup message dialog."""
        ThemePopup(title, msg, color)

    def scan_for_profiles(self):
        """Scan default Icarus installation directory for player profiles."""
        appdata = os.getenv('LOCALAPPDATA')
        if not appdata: return {}
        base_path = os.path.join(appdata, 'Icarus', 'Saved', 'PlayerData')
        profiles = {}
        if os.path.exists(base_path):
            for folder in os.listdir(base_path):
                full_path = os.path.join(base_path, folder)
                if os.path.isdir(full_path) and folder.isdigit():
                    profiles[folder] = full_path
        return profiles

    def browse_folder(self):
        """Open file dialog to manually select a player data folder."""
        folder_selected = filedialog.askdirectory(title="SELECT ICARUS PLAYER DATA FOLDER")
        if folder_selected:
            p_check = os.path.join(folder_selected, "Profile.json")
            if os.path.exists(p_check):
                folder_name = os.path.basename(folder_selected)
                self.profiles_map[folder_name] = folder_selected
                self.profile_dropdown.configure(values=list(self.profiles_map.keys()))
                self.profile_dropdown.set(folder_name)
                self.current_folder_path = folder_selected
                self.load_data()
                self.btn_save.configure(state="normal")
                self.show_message("SUCCESS", f"Profile loaded successfully:\n{folder_name}")
            else:
                self.show_message("INVALID FOLDER", "Folder must contain Profile.json!", "#FF5555")

    def create_widgets(self):
        self.header_frame = ctk.CTkFrame(self, fg_color=COL_BG_PANEL, border_width=1, border_color=COL_BORDER, corner_radius=0, height=80)
        self.header_frame.pack(fill="x", side="top", padx=1, pady=1)
        ctk.CTkLabel(self.header_frame, text="LUMEN // EDITOR", font=("Impact", 28), text_color=COL_TEXT_LIGHT).pack(side="left", padx=30, pady=20)

        ctrl_frame = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        ctrl_frame.pack(side="right", padx=30)

        self.btn_browse = ctk.CTkButton(
            ctrl_frame, text="[ BROWSE ]", width=100, command=self.browse_folder,
            fg_color=COL_BG_INPUT, hover_color=COL_BORDER, border_width=1, border_color=COL_BORDER, text_color=COL_TEXT_LIGHT
        )
        self.btn_browse.pack(side="right", padx=10)

        self.profile_dropdown = ctk.CTkOptionMenu(
            ctrl_frame, values=list(self.profiles_map.keys()) if self.profiles_map else ["NO PROFILE"],
            command=self.change_profile, width=200, fg_color=COL_BG_INPUT, button_color=COL_BORDER,
            button_hover_color=COL_ACCENT_GOLD, text_color=COL_TEXT_LIGHT, dropdown_fg_color=COL_BG_PANEL, dropdown_text_color=COL_TEXT_LIGHT,
            corner_radius=2
        )
        self.profile_dropdown.pack(side="right", padx=5)
        ctk.CTkLabel(ctrl_frame, text="ID:", font=("Arial", 10, "bold"), text_color=COL_BORDER).pack(side="right", padx=5)

        self.frame = ctk.CTkFrame(self, width=600, corner_radius=0, fg_color="transparent")
        self.frame.pack(pady=10, padx=0, fill="both", expand=True)

        self.footer_frame = ctk.CTkFrame(self, fg_color=COL_BG_PANEL, border_width=1, border_color=COL_BORDER, corner_radius=0, height=90)
        self.footer_frame.pack(fill="x", side="bottom", padx=1, pady=1)

        self.status_label = ctk.CTkLabel(self.footer_frame, text="WAITING...", font=("Consolas", 12), text_color=COL_BORDER)
        self.status_label.pack(side="left", padx=30)

        self.btn_save = ctk.CTkButton(
            self.footer_frame, text="[ SAVE & APPLY ]", command=self.save_data, width=220, height=45,
            font=("Arial", 13, "bold"), fg_color=COL_ACCENT_GOLD, hover_color="#b59840", text_color=COL_TEXT_DARK, corner_radius=2
        )
        self.btn_save.pack(side="right", padx=30, pady=20)
        
        self.btn_refresh = ctk.CTkButton(
            self.footer_frame, text="RELOAD", command=self.refresh_current_profile, width=100, height=45,
            font=("Arial", 12, "bold"), fg_color=COL_BG_INPUT, hover_color=COL_BORDER, text_color=COL_TEXT_LIGHT, border_width=1, border_color=COL_BORDER, corner_radius=2
        )
        self.btn_refresh.pack(side="right", padx=10)

    def change_profile(self, selected_id):
        """Switch to a different player profile."""
        if selected_id in self.profiles_map:
            self.current_folder_path = self.profiles_map[selected_id]
            self.load_data()
        else:
            self.current_folder_path = None

    def refresh_current_profile(self):
        """Reload data from the currently selected profile."""
        if self.current_folder_path:
            self.load_data()
            self.status_label.configure(text="DATA RELOADED", text_color=C_LIC)

    def clear_ui(self):
        """Remove all widgets from the main content frame."""
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.entries.clear()

    def add_section_header(self, text):
        """Create a styled section header with accent bar."""
        container = ctk.CTkFrame(self.frame, fg_color="transparent")
        container.pack(fill="x", pady=(25, 5), padx=30)
        ctk.CTkFrame(container, width=3, height=18, fg_color=COL_ACCENT_GOLD, corner_radius=0).pack(side="left")
        ctk.CTkLabel(container, text=text, font=("Arial", 16, "bold"), text_color=COL_TEXT_LIGHT).pack(side="left", padx=10)
        ctk.CTkFrame(self.frame, height=1, fg_color=COL_BORDER, corner_radius=0).pack(fill="x", padx=30, pady=0)

    def add_input_field(self, label_text, key_id, value, section, icon_color=None):
        """Create a labeled input field with optional colored accent bar."""
        row = ctk.CTkFrame(self.frame, fg_color=COL_BG_PANEL, border_width=1, border_color=COL_BORDER, corner_radius=2)
        row.pack(fill="x", pady=4, padx=30)
        
        if icon_color: ctk.CTkFrame(row, width=4, height=45, corner_radius=0, fg_color=icon_color).pack(side="left")
        else: ctk.CTkFrame(row, width=4, height=45, corner_radius=0, fg_color="transparent").pack(side="left")

        ctk.CTkLabel(row, text=label_text.upper(), font=("Arial", 11, "bold"), text_color=COL_TEXT_LIGHT, anchor="w", width=220).pack(side="left", padx=15)
        
        entry = ctk.CTkEntry(
            row, font=("Consolas", 15), fg_color=COL_BG_INPUT, border_width=0, corner_radius=0,
            text_color=COL_TEXT_LIGHT, justify="right"
        )
        val_str = str(value) if value is not None else "0"
        entry.insert(0, val_str)
        entry.pack(side="right", padx=15, pady=10, fill="x", expand=True)
        
        self.entries[f"{section}|{key_id}"] = entry
        return entry

    def add_level_manager(self, current_xp, section):
        """Create the level/XP management widget with progress bar and calculators."""
        container = ctk.CTkFrame(self.frame, fg_color=COL_BG_PANEL, border_width=1, border_color=COL_BORDER, corner_radius=2)
        container.pack(fill="x", pady=5, padx=30)
        
        head = ctk.CTkFrame(container, fg_color="transparent")
        head.pack(fill="x", padx=15, pady=10)
        ctk.CTkLabel(head, text="LEVEL MANAGER", font=("Arial", 11, "bold"), text_color=COL_ACCENT_GOLD).pack(side="left")

        controls = ctk.CTkFrame(container, fg_color="transparent")
        controls.pack(fill="x", padx=10, pady=5)
        
        left_box = ctk.CTkFrame(controls, fg_color="transparent")
        left_box.pack(side="left", fill="x", expand=True)
        ctk.CTkLabel(left_box, text="TARGET LEVEL", font=("Arial", 9, "bold"), text_color=COL_BORDER).pack(anchor="w")
        self.lvl_entry_ref = ctk.CTkEntry(left_box, width=60, font=("Consolas", 14), fg_color=COL_BG_INPUT, border_width=0, justify="center", text_color=COL_TEXT_LIGHT)
        self.lvl_entry_ref.pack(side="left", pady=2)
        ctk.CTkButton(left_box, text="CALC XP ->", width=90, command=self.calc_xp_from_lvl, corner_radius=2, fg_color=COL_BORDER, hover_color=COL_BG_INPUT, text_color=COL_TEXT_LIGHT).pack(side="left", padx=5)

        right_box = ctk.CTkFrame(controls, fg_color="transparent")
        right_box.pack(side="right", fill="x", expand=True)
        ctk.CTkLabel(right_box, text="CUSTOM XP", font=("Arial", 9, "bold"), text_color=COL_BORDER).pack(anchor="w")
        self.xp_entry_ref = ctk.CTkEntry(right_box, font=("Consolas", 14), fg_color=COL_BG_INPUT, border_width=0, justify="right", text_color=COL_TEXT_LIGHT)
        self.xp_entry_ref.insert(0, str(current_xp))
        self.xp_entry_ref.pack(side="left", fill="x", expand=True, pady=2)
        ctk.CTkButton(right_box, text="<- GET LVL", width=90, command=self.calc_lvl_from_xp, corner_radius=2, fg_color=COL_BORDER, hover_color=COL_BG_INPUT, text_color=COL_TEXT_LIGHT).pack(side="left", padx=5)

        self.entries[f"{section}|XP"] = self.xp_entry_ref

        bar_frame = ctk.CTkFrame(container, fg_color="transparent")
        bar_frame.pack(fill="x", padx=15, pady=(15, 20))
        self.progress_label_ref = ctk.CTkLabel(bar_frame, text="LEVEL PROGRESS", font=("Arial", 10, "bold"), text_color=COL_TEXT_LIGHT, anchor="w")
        self.progress_label_ref.pack(fill="x", pady=(0, 4))
        self.progress_bar_ref = ctk.CTkProgressBar(bar_frame, height=14, corner_radius=0, fg_color=COL_BORDER, progress_color=COL_TEXT_LIGHT)
        self.progress_bar_ref.set(0)
        self.progress_bar_ref.pack(fill="x")
        self.update_progress_visuals(current_xp)

    def calc_xp_from_lvl(self):
        """Calculate required XP for a given level using Icarus formula: XP = 1570 * level²"""
        try:
            lvl = int(self.lvl_entry_ref.get())
            if lvl < 1: lvl = 1
            if lvl > 150: lvl = 150
            new_xp = int(1570 * (lvl ** 2))
            
            self.xp_entry_ref.delete(0, "end")
            self.xp_entry_ref.insert(0, str(new_xp))
            self.update_progress_visuals(new_xp)
            self.status_label.configure(text=f"SET TO LEVEL {lvl}", text_color=COL_TEXT_LIGHT)
        except ValueError:
            pass

    def calc_lvl_from_xp(self):
        """Calculate level from XP using inverse formula: level = √(XP / 1570)"""
        try:
            raw_xp = int(self.xp_entry_ref.get())
            lvl = int(math.sqrt(raw_xp / 1570))
            if lvl < 1: lvl = 1
            self.lvl_entry_ref.delete(0, "end")
            self.lvl_entry_ref.insert(0, str(lvl))
            self.update_progress_visuals(raw_xp)
            self.status_label.configure(text=f"XP MATCHES LEVEL {lvl}", text_color=COL_TEXT_LIGHT)
        except ValueError:
            pass

    def update_progress_visuals(self, current_xp):
        """Update progress bar and label to show current level progress."""
        try:
            current_xp = int(current_xp)
            current_lvl = int(math.sqrt(current_xp / 1570))
            xp_start_of_lvl = int(1570 * (current_lvl ** 2))
            xp_start_of_next = int(1570 * ((current_lvl + 1) ** 2))
            range_span = xp_start_of_next - xp_start_of_lvl
            if range_span <= 0: range_span = 1
            progress_val = (current_xp - xp_start_of_lvl) / range_span
            if progress_val < 0: progress_val = 0
            if progress_val > 1: progress_val = 1
            self.progress_bar_ref.set(progress_val)
            pct = int(progress_val * 100)
            txt = f"LEVEL {current_lvl}  >>  {pct}%  >>  LEVEL {current_lvl + 1}"
            self.progress_label_ref.configure(text=txt)
        except:
            pass

    def load_data(self):
        """Load and display profile and character data from JSON files."""
        if not self.current_folder_path or not os.path.exists(self.current_folder_path): return
        self.clear_ui()

        # Load Profile.json (account wallet/currencies)
        p_path = os.path.join(self.current_folder_path, 'Profile.json')
        if os.path.exists(p_path):
            try:
                with open(p_path, 'r', encoding='utf-8') as f:
                    self.profile_data = json.load(f)
                self.add_section_header("ACCOUNT WALLET")
                
                currency_config = {
                    "Refund":     {"label": "RESPEC POINTS", "color": C_REF},
                    "Credits":    {"label": "REN", "color": C_REN},
                    "Exotic1":    {"label": "EXOTICS", "color": C_EXO},
                    "Exotic_Red": {"label": "STABILIZED", "color": C_RED},
                    "Biomass":    {"label": "LEGENDARY BIOMASS", "color": C_BIO},
                    "licence":    {"label": "LEGENDARY LICENSE", "color": C_LIC}, 
                }
                meta = self.profile_data.get("MetaResources", [])
                
                # Track which currencies have been added to avoid duplicates
                added_labels = [] 
                
                for item in meta:
                    key = item.get("MetaRow")
                    if key in currency_config:
                        conf = currency_config[key]
                        if conf["label"] not in added_labels:
                            self.add_input_field(conf["label"], key, item.get("Count", 0), "PROFILE", icon_color=conf["color"])
                            added_labels.append(conf["label"])
                
                # Add missing currencies with zero value
                for key, conf in currency_config.items():
                    if conf["label"] not in added_labels:
                        self.add_input_field(conf["label"], key, 0, "PROFILE_NEW", icon_color=conf["color"])
                        added_labels.append(conf["label"])

            except Exception as e:
                self.show_message("ERROR", f"Failed to load Profile:\n{e}", "#FF5555")

        # Load Characters.json (character XP and stats)
        c_path = os.path.join(self.current_folder_path, 'Characters.json')
        if os.path.exists(c_path):
            try:
                with open(c_path, 'r', encoding='utf-8') as f:
                    container = json.load(f)
                self.char_container = container
                raw_char_data = None
                
                # Handle different JSON structure formats (list or dict)
                if isinstance(container, list) and len(container) > 0:
                    self.char_key_or_index = 0
                    raw_char_data = container[0]
                elif isinstance(container, dict) and len(container) > 0:
                    first_key = next(iter(container))
                    self.char_key_or_index = first_key
                    raw_char_data = container[first_key]
                
                # Handle nested list structure
                if isinstance(raw_char_data, list) and len(raw_char_data) > 0:
                    raw_char_data = raw_char_data[0]
                    self.char_is_nested_list = True
                else:
                    self.char_is_nested_list = False
                
                # Parse character data (may be JSON string or dict)
                final_char_obj = {}
                if isinstance(raw_char_data, str):
                    try: 
                        final_char_obj = json.loads(raw_char_data)
                        self.char_is_encoded_string = True
                    except: 
                        pass
                elif isinstance(raw_char_data, dict):
                    final_char_obj = raw_char_data
                    self.char_is_encoded_string = False
                
                if final_char_obj:
                    name = final_char_obj.get("CharacterName", "UNKNOWN").upper()
                    self.add_section_header(f"CHARACTER: {name}")
                    current_xp = final_char_obj.get("XP", 0)
                    self.add_level_manager(current_xp, "CHAR")
                    try:
                        lvl_calc = int(math.sqrt(current_xp / 1570))
                        if self.lvl_entry_ref:
                            self.lvl_entry_ref.delete(0, "end")
                            self.lvl_entry_ref.insert(0, str(lvl_calc))
                    except: pass
            except Exception as e:
                self.show_message("ERROR", f"Failed to load Characters:\n{e}", "#FF5555")

        self.status_label.configure(text=f"CONNECTED: {os.path.basename(self.current_folder_path)}", text_color=C_BIO)

    def save_data(self):
        """Save modified data to JSON files with automatic backup creation."""
        if not self.current_folder_path: return
        try:
            p_path = os.path.join(self.current_folder_path, 'Profile.json')
            if os.path.exists(p_path):
                # Create backup before modifying
                shutil.copy(p_path, p_path + ".backup") 
                # Update existing currency values
                meta = self.profile_data.get("MetaResources", [])
                for key_full, entry in list(self.entries.items()):
                    section, r_key = key_full.split("|")
                    try: 
                        val = int(entry.get())
                    except: 
                        continue
                    if section == "PROFILE":
                        # Update existing currency
                        for item in meta:
                            if item["MetaRow"] == r_key: 
                                item["Count"] = val
                    elif section == "PROFILE_NEW" and val > 0:
                        # Add new currency entry
                        meta.append({"MetaRow": r_key, "Count": val})
                self.profile_data["MetaResources"] = meta
                with open(p_path, 'w', encoding='utf-8') as f: json.dump(self.profile_data, f, indent=4)

            c_path = os.path.join(self.current_folder_path, 'Characters.json')
            if self.char_container is not None and os.path.exists(c_path):
                # Create backup before modifying
                shutil.copy(c_path, c_path + ".backup")
                
                # Extract character data using stored structure info
                raw_data = self.char_container[self.char_key_or_index]
                if self.char_is_nested_list and isinstance(raw_data, list): 
                    item_to_edit = raw_data[0]
                else: 
                    item_to_edit = raw_data
                
                # Parse character object (may be JSON string or dict)
                char_obj = {}
                if self.char_is_encoded_string and isinstance(item_to_edit, str): 
                    char_obj = json.loads(item_to_edit)
                elif isinstance(item_to_edit, dict): 
                    char_obj = item_to_edit
                
                # Apply user changes to character data
                for key_full, entry in list(self.entries.items()):
                    section, r_key = key_full.split("|")
                    if section == "CHAR":
                        try: 
                            char_obj[r_key] = int(entry.get())
                        except: 
                            pass
                        
                # Reconstruct character data in original format
                final_element = char_obj
                if self.char_is_encoded_string: 
                    final_element = json.dumps(char_obj)
                if self.char_is_nested_list: 
                    self.char_container[self.char_key_or_index][0] = final_element
                else: 
                    self.char_container[self.char_key_or_index] = final_element
                with open(c_path, 'w', encoding='utf-8') as f: json.dump(self.char_container, f, indent=4)

            self.status_label.configure(text="SUCCESSFUL WRITE", text_color=C_BIO)
            self.show_message("SUCCESS", "Data saved successfully!\n\n(Restart game to see changes.)", C_BIO)

        except PermissionError:
             self.show_message("SAVE FAILED", "File is locked by Icarus.\nPlease close the game.", "#FF5555")
        except Exception as e:
            self.show_message("ERROR", f"Error saving data:\n{e}", "#FF5555")

if __name__ == "__main__":
    app = LumenIcarusEditor()
>>>>>>> 4d0f01816fe7662521df37a00297a2d3487fe3ad
    app.mainloop()